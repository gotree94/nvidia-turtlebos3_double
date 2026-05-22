#!/usr/bin/env python3
"""
Digital Twin - Real-world Data Logger

실제 로봇의 주행 데이터를 수집하여 Episode DB에 저장합니다.
ROS2 bag 대신 경량 SQLite 기반으로 설계되어 디지털 트윈 루프에 최적화.

Usage:
    ros2 run digital_twin data_logger
    # 또는 직접 실행:
    python3 src/digital_twin/data_logger.py
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import LaserScan, Image
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32MultiArray, String
import sqlite3
import json
import time
import os
import uuid
import numpy as np
from datetime import datetime
from threading import Lock


class EpisodeDB:
    """
    경험 데이터베이스 (SQLite 기반)
    
    디지털 트윈 루프의 핵심 저장소:
    - episode: 주행 에피소드 메타데이터
    - transitions: (상태, 행동, 보상, 다음상태) 전이 데이터
    - metrics: 에피소드별 성능 메트릭
    
    Schema:
        episodes(
            id TEXT PK, robot_id TEXT, policy_id TEXT,
            start_time REAL, end_time REAL, success BOOL,
            goal_x REAL, goal_y REAL, env_config TEXT
        )
        transitions(
            id TEXT PK, episode_id TEXT FK,
            timestamp REAL, lidar BLOB, goal_rel BLOB,
            heading_err REAL, linear_vel REAL, angular_vel REAL,
            reward REAL, done BOOL
        )
        metrics(
            episode_id TEXT PK FK,
            path_length REAL, avg_linear_vel REAL, avg_angular_vel REAL,
            min_lidar REAL, collisions INT, success BOOL
        )
    """
    
    def __init__(self, db_path: str = "data/episode_db.sqlite"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True) if os.path.dirname(db_path) else None
        self.db_path = db_path
        self.lock = Lock()
        self._init_db()
        print(f"[EpisodeDB] Initialized: {db_path}")
    
    def _init_db(self):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS episodes (
                    id TEXT PRIMARY KEY,
                    robot_id TEXT NOT NULL,
                    policy_id TEXT NOT NULL,
                    start_time REAL NOT NULL,
                    end_time REAL,
                    success BOOL DEFAULT 0,
                    goal_x REAL,
                    goal_y REAL,
                    env_config TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS transitions (
                    id TEXT PRIMARY KEY,
                    episode_id TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    lidar BLOB,
                    goal_rel BLOB,
                    heading_err REAL,
                    linear_vel REAL,
                    angular_vel REAL,
                    reward REAL DEFAULT 0,
                    done BOOL DEFAULT 0,
                    FOREIGN KEY (episode_id) REFERENCES episodes(id)
                );
                CREATE TABLE IF NOT EXISTS metrics (
                    episode_id TEXT PRIMARY KEY,
                    path_length REAL DEFAULT 0,
                    avg_linear_vel REAL DEFAULT 0,
                    avg_angular_vel REAL DEFAULT 0,
                    min_lidar REAL DEFAULT 3.5,
                    collisions INT DEFAULT 0,
                    success BOOL DEFAULT 0,
                    FOREIGN KEY (episode_id) REFERENCES episodes(id)
                );
                CREATE INDEX IF NOT EXISTS idx_episode_robot ON episodes(robot_id);
                CREATE INDEX IF NOT EXISTS idx_episode_policy ON episodes(policy_id);
                CREATE INDEX IF NOT EXISTS idx_transitions_episode ON transitions(episode_id);
            """)
    
    def create_episode(self, robot_id: str, policy_id: str, goal: tuple = None) -> str:
        episode_id = str(uuid.uuid4())
        with self.lock, sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO episodes (id, robot_id, policy_id, start_time, goal_x, goal_y) VALUES (?, ?, ?, ?, ?, ?)",
                (episode_id, robot_id, policy_id, time.time(),
                 goal[0] if goal else None, goal[1] if goal else None)
            )
        return episode_id
    
    def end_episode(self, episode_id: str, success: bool):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE episodes SET end_time = ?, success = ? WHERE id = ?",
                (time.time(), int(success), episode_id)
            )
    
    def record_transition(self, episode_id: str, obs: dict, action: np.ndarray, reward: float, done: bool):
        trans_id = str(uuid.uuid4())
        lidar_blob = json.dumps(obs.get("lidar", []).tolist() if hasattr(obs.get("lidar", []), 'tolist') else list(obs.get("lidar", [])))
        goal_blob = json.dumps(list(obs.get("goal_rel", [0, 0])))
        
        with self.lock, sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO transitions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (trans_id, episode_id, time.time(),
                 lidar_blob, goal_blob, obs.get("heading_err", 0),
                 float(action[0]), float(action[1]),
                 float(reward), int(done))
            )
    
    def update_metrics(self, episode_id: str, metrics: dict):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO metrics 
                (episode_id, path_length, avg_linear_vel, avg_angular_vel, min_lidar, collisions, success)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (episode_id, metrics.get("path_length", 0), metrics.get("avg_linear_vel", 0),
                  metrics.get("avg_angular_vel", 0), metrics.get("min_lidar", 3.5),
                  metrics.get("collisions", 0), int(metrics.get("success", False))))
    
    def get_recent_episodes(self, limit: int = 100, policy_id: str = None) -> list:
        with self.lock, sqlite3.connect(self.db_path) as conn:
            if policy_id:
                rows = conn.execute(
                    "SELECT * FROM episodes WHERE policy_id = ? ORDER BY start_time DESC LIMIT ?",
                    (policy_id, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM episodes ORDER BY start_time DESC LIMIT ?", (limit,)
                ).fetchall()
        return rows
    
    def get_success_rate(self, policy_id: str, recent_n: int = 50) -> float:
        with self.lock, sqlite3.connect(self.db_path) as conn:
            row = conn.execute("""
                SELECT AVG(success) FROM (
                    SELECT success FROM episodes 
                    WHERE policy_id = ? AND end_time IS NOT NULL 
                    ORDER BY start_time DESC LIMIT ?
                )
            """, (policy_id, recent_n)).fetchone()
        return row[0] if row and row[0] else 0.0
    
    def export_for_training(self, policy_id: str, limit: int = 1000) -> dict:
        """재학습용 데이터 내보내기"""
        with self.lock, sqlite3.connect(self.db_path) as conn:
            transitions = conn.execute("""
                SELECT t.lidar, t.goal_rel, t.heading_err, 
                       t.linear_vel, t.angular_vel, t.reward, t.done
                FROM transitions t
                JOIN episodes e ON t.episode_id = e.id
                WHERE e.policy_id = ? AND e.success = 1
                ORDER BY t.timestamp DESC LIMIT ?
            """, (policy_id, limit)).fetchall()
        
        return {
            "policy_id": policy_id,
            "num_samples": len(transitions),
            "data": [{
                "lidar": json.loads(t[0]),
                "goal_rel": json.loads(t[1]),
                "heading_err": t[2],
                "linear_vel": t[3],
                "angular_vel": t[4],
                "reward": t[5],
                "done": bool(t[6]),
            } for t in transitions]
        }


class RealWorldDataLogger(Node):
    """
    실제 로봇 주행 데이터 수집 노드
    
    - /cmd_vel, /odom, /scan, /policy/debug 구독
    - 에피소드 단위로 EpisodeDB에 저장
    - 자동 에피소드 경계 감지 (목표 도달 / 충돌 / 타임아웃)
    """
    
    def __init__(self):
        super().__init__('digital_twin_data_logger')
        
        # ========== 파라미터 ==========
        self.declare_parameter('db_path', 'data/episode_db.sqlite')
        self.declare_parameter('robot_id', 'jetson_orin_nano')
        self.declare_parameter('policy_id', 'policy_latest')
        self.declare_parameter('max_episode_steps', 1000)
        self.declare_parameter('episode_timeout', 120.0)  # seconds
        
        # ========== DB 초기화 ==========
        self.db = EpisodeDB(
            db_path=self.get_parameter('db_path').value
        )
        self.robot_id = self.get_parameter('robot_id').value
        self.policy_id = self.get_parameter('policy_id').value
        self.max_steps = self.get_parameter('max_episode_steps').value
        self.episode_timeout = self.get_parameter('episode_timeout').value
        
        # ========== 에피소드 상태 ==========
        self.current_episode_id = None
        self.episode_step = 0
        self.episode_start_time = None
        self.episode_path_length = 0.0
        self.episode_linear_v = []
        self.episode_angular_v = []
        self.episode_min_lidar = 3.5
        self.episode_collisions = 0
        self.last_position = None
        self.goal_position = None
        
        # ========== 최신 센서 데이터 ==========
        self.latest_scan = None
        self.latest_odom = None
        self.latest_action = np.array([0.0, 0.0])
        self.robot_position = (0.0, 0.0)
        self.robot_yaw = 0.0
        
        # ========== QoS ==========
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        
        # ========== Subscribers ==========
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, qos)
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, qos)
        self.cmd_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_callback, 10)
        self.goal_sub = self.create_subscription(
            PoseStamped, '/goal_pose', self.goal_callback, 10)
        self.debug_sub = self.create_subscription(
            Float32MultiArray, '/policy/debug', self.debug_callback, 10)
        
        # ========== Publishers ==========
        self.episode_event_pub = self.create_publisher(
            String, '/digital_twin/episode_event', 10)
        
        # ========== 타이머 ==========
        self.create_timer(0.1, self.control_loop)  # 10Hz
        self.create_timer(5.0, self.status_report)  # 5초마다 상태 보고
        
        self.get_logger().info(
            f'[DataLogger] Started | robot={self.robot_id} policy={self.policy_id}'
        )
    
    def scan_callback(self, msg: LaserScan):
        self.latest_scan = msg
    
    def odom_callback(self, msg: Odometry):
        self.latest_odom = msg
        pos = msg.pose.pose.position
        self.robot_position = (pos.x, pos.y)
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.robot_yaw = np.arctan2(siny, cosy)
    
    def cmd_callback(self, msg: Twist):
        self.latest_action = np.array([msg.linear.x, msg.angular.z])
    
    def goal_callback(self, msg: PoseStamped):
        self.goal_position = (msg.pose.position.x, msg.pose.position.y)
    
    def debug_callback(self, msg: Float32MultiArray):
        pass  # 확장 포인트
    
    def _check_episode_boundary(self) -> str:
        """
        에피소드 경계 감지
        
        Returns:
            'goal_reached' | 'collision' | 'timeout' | 'running'
        """
        if self.latest_scan is None or self.latest_odom is None:
            return 'running'
        
        # 목표 도달
        if self.goal_position:
            dx = self.goal_position[0] - self.robot_position[0]
            dy = self.goal_position[1] - self.robot_position[1]
            dist = np.sqrt(dx*dx + dy*dy)
            if dist < 0.2:
                return 'goal_reached'
        
        # 충돌 감지
        ranges = np.array(self.latest_scan.ranges)
        ranges = np.nan_to_num(ranges, nan=3.5)
        min_dist = np.min(ranges)
        self.episode_min_lidar = min(min(self.episode_min_lidar, min_dist), 
                                      self.episode_min_lidar)
        if min_dist < 0.15:
            self.episode_collisions += 1
            if self.episode_collisions >= 3:
                return 'collision'
        
        # 타임아웃
        if self.episode_start_time and \
           (time.time() - self.episode_start_time) > self.episode_timeout:
            return 'timeout'
        
        # 최대 스텝
        if self.episode_step >= self.max_steps:
            return 'timeout'
        
        return 'running'
    
    def _start_new_episode(self):
        """새 에피소드 시작"""
        self.current_episode_id = self.db.create_episode(
            robot_id=self.robot_id,
            policy_id=self.policy_id,
            goal=self.goal_position
        )
        self.episode_step = 0
        self.episode_start_time = time.time()
        self.episode_path_length = 0.0
        self.episode_linear_v = []
        self.episode_angular_v = []
        self.episode_min_lidar = 3.5
        self.episode_collisions = 0
        self.last_position = self.robot_position
        
        # 이벤트 발행
        msg = String()
        msg.data = json.dumps({
            "event": "episode_start",
            "episode_id": self.current_episode_id,
            "policy_id": self.policy_id,
            "timestamp": time.time(),
        })
        self.episode_event_pub.publish(msg)
        
        self.get_logger().info(
            f'[Episode] START | id={self.current_episode_id[:8]}... '
            f'policy={self.policy_id}'
        )
    
    def _end_current_episode(self, status: str):
        """현재 에피소드 종료"""
        if not self.current_episode_id:
            return
        
        success = (status == 'goal_reached')
        
        # 에피소드 종료
        self.db.end_episode(self.current_episode_id, success)
        
        # 메트릭 저장
        metrics = {
            "path_length": self.episode_path_length,
            "avg_linear_vel": np.mean(self.episode_linear_v) if self.episode_linear_v else 0,
            "avg_angular_vel": np.mean(self.episode_angular_v) if self.episode_angular_v else 0,
            "min_lidar": self.episode_min_lidar,
            "collisions": self.episode_collisions,
            "success": success,
        }
        self.db.update_metrics(self.current_episode_id, metrics)
        
        # 이벤트 발행
        msg = String()
        msg.data = json.dumps({
            "event": "episode_end",
            "episode_id": self.current_episode_id,
            "status": status,
            "success": success,
            "metrics": metrics,
            "timestamp": time.time(),
        })
        self.episode_event_pub.publish(msg)
        
        self.get_logger().info(
            f'[Episode] END   | id={self.current_episode_id[:8]}... '
            f'status={status} success={success} '
            f'steps={self.episode_step} path={self.episode_path_length:.2f}m'
        )
        
        self.current_episode_id = None
    
    def control_loop(self):
        """메인 제어 루프 (10Hz)"""
        # 경계 조건 확인
        status = self._check_episode_boundary()
        
        # 에피소드 종료/시작
        if status != 'running' and self.current_episode_id:
            self._end_current_episode(status)
        
        if not self.current_episode_id and self.latest_odom is not None:
            self._start_new_episode()
        
        # 전이 기록
        if self.current_episode_id and self.latest_scan is not None:
            ranges = np.array(self.latest_scan.ranges)
            ranges = np.nan_to_num(ranges, nan=3.5)
            ranges = np.clip(ranges, 0.15, 3.5) / 3.5
            lidar_down = np.mean(ranges.reshape(36, 10), axis=1)
            
            # goal relative
            if self.goal_position:
                dx = self.goal_position[0] - self.robot_position[0]
                dy = self.goal_position[1] - self.robot_position[1]
            else:
                dx, dy = 1.0, 0.0
            
            obs = {
                "lidar": lidar_down,
                "goal_rel": np.array([dx, dy]) / 8.0,
                "heading_err": 0.0,  # 간소화
            }
            
            self.db.record_transition(
                self.current_episode_id, obs,
                self.latest_action, 0.0, status != 'running'
            )
            
            # 경로 길이 업데이트
            if self.last_position:
                dx = self.robot_position[0] - self.last_position[0]
                dy = self.robot_position[1] - self.last_position[1]
                self.episode_path_length += np.sqrt(dx*dx + dy*dy)
            self.last_position = self.robot_position
            
            self.episode_linear_v.append(abs(self.latest_action[0]))
            self.episode_angular_v.append(abs(self.latest_action[1]))
            self.episode_step += 1
    
    def status_report(self):
        """정기 상태 보고"""
        if self.current_episode_id:
            success_rate = self.db.get_success_rate(self.policy_id, recent_n=50)
            total_episodes = len(self.db.get_recent_episodes(limit=1000, policy_id=self.policy_id))
            self.get_logger().info(
                f'[Status] episode={self.episode_step}steps '
                f'success_rate={success_rate:.1%} '
                f'total_episodes={total_episodes}'
            )


def main(args=None):
    rclpy.init(args=args)
    node = RealWorldDataLogger()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
