#!/bin/bash
# ============================================
# Digital Twin - Blue-Green Policy Deployment
# ============================================
# Usage:
#   bash scripts/deploy_policy.sh <policy.plan> [policy_id]
#   bash scripts/deploy_policy.sh --rollback
#   bash scripts/deploy_policy.sh --status
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY_FILE="${SCRIPT_DIR}/config/policy_registry.json"
DEPLOY_DIR="${SCRIPT_DIR}/deployed_policies"
ACTIVE_LINK="${DEPLOY_DIR}/active"
BACKUP_DIR="${DEPLOY_DIR}/backup"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

mkdir -p "$DEPLOY_DIR"
mkdir -p "$(dirname "$REGISTRY_FILE")"

# ========== Functions ==========

status() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  Policy Deployment Status${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    if [ -L "$ACTIVE_LINK" ]; then
        ACTUAL=$(readlink -f "$ACTIVE_LINK")
        POLICY_ID=$(basename "$ACTUAL")
        echo -e "  ${GREEN}✅ Active:${NC} $POLICY_ID"
        if [ -f "$ACTUAL/policy.plan" ]; then
            SIZE=$(du -h "$ACTUAL/policy.plan" | cut -f1)
            echo -e "  Size:  $SIZE"
        fi
    else
        echo -e "  ${RED}❌ No active policy${NC}"
    fi
    
    echo ""
    echo -e "  ${YELLOW}Available policies:${NC}"
    for dir in "$DEPLOY_DIR"/*/; do
        if [ -d "$dir" ] && [ ! -L "$dir" ]; then
            PID=$(basename "$dir")
            if [ -f "$dir/deploy_event.json" ]; then
                SR=$(python3 -c "import json; d=json.load(open('$dir/deploy_event.json')); print(f\"SR={d['evaluation']['success_rate']:.0%}\")" 2>/dev/null || echo "no eval")
                echo -e "    📦 $PID ($SR)"
            else
                echo -e "    📦 $PID"
            fi
        fi
    done
    
    if [ -d "$BACKUP_DIR" ] && [ -L "$BACKUP_DIR/previous" ]; then
        BACKUP_ID=$(basename "$(readlink -f "$BACKUP_DIR/previous")")
        echo -e "  ${YELLOW}Backup:${NC} $BACKUP_ID"
    fi
    
    echo -e "${BLUE}========================================${NC}\n"
}

deploy() {
    MODEL_PATH="$1"
    POLICY_ID="${2:-policy_$(date +%Y%m%d_%H%M%S)}"
    
    if [ ! -f "$MODEL_PATH" ]; then
        echo -e "${RED}❌ Model not found: $MODEL_PATH${NC}"
        exit 1
    fi
    
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  Deploying Policy${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "  Model:    $MODEL_PATH"
    echo -e "  Policy:   $POLICY_ID"
    echo -e "${BLUE}========================================${NC}\n"
    
    # 1. 배포 디렉토리 생성
    POLICY_DIR="${DEPLOY_DIR}/${POLICY_ID}"
    mkdir -p "$POLICY_DIR"
    
    # 2. 모델 복사
    cp "$MODEL_PATH" "$POLICY_DIR/policy.plan"
    echo -e "  ${GREEN}✅${NC} Model copied"
    
    # 3. 현재 active → backup
    if [ -L "$ACTIVE_LINK" ]; then
        CURRENT_ACTIVE=$(readlink -f "$ACTIVE_LINK")
        if [ -d "$CURRENT_ACTIVE" ]; then
            mkdir -p "$BACKUP_DIR"
            ln -sfn "$CURRENT_ACTIVE" "$BACKUP_DIR/previous"
            echo -e "  ${YELLOW}📦${NC} Previous active → backup"
        fi
    fi
    
    # 4. 블루-그린 전환 (심볼릭 링크 변경)
    # 새 디렉토리로 링크
    ln -sfn "$POLICY_DIR" "$ACTIVE_LINK"
    echo -e "  ${GREEN}✅${NC} Blue-Green switch complete"
    
    # 5. ROS2 노드 재시작 (있는 경우)
    if systemctl is-active --quiet turtlebot3-policy 2>/dev/null; then
        sudo systemctl restart turtlebot3-policy
        echo -e "  ${GREEN}✅${NC} Policy service restarted"
    fi
    
    # 6. 레지스트리 업데이트
    TIMESTAMP=$(date -Iseconds)
    if command -v python3 &> /dev/null; then
        python3 -c "
import json
reg_path = '$REGISTRY_FILE'
try:
    with open(reg_path) as f:
        reg = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    reg = {'policies': {}, 'active_policy': None, 'history': []}

reg['policies']['$POLICY_ID'] = {
    'policy_id': '$POLICY_ID',
    'checkpoint': '$POLICY_DIR/policy.plan',
    'status': 'active',
    'deployed_at': '$TIMESTAMP',
}

# 이전 active → backup
old_active = reg.get('active_policy')
if old_active and old_active in reg['policies']:
    reg['policies'][old_active]['status'] = 'backup'

reg['active_policy'] = '$POLICY_ID'
reg['history'].append({
    'event': 'deploy',
    'policy_id': '$POLICY_ID',
    'timestamp': '$TIMESTAMP',
})

with open(reg_path, 'w') as f:
    json.dump(reg, f, indent=2)
print('Registry updated')
"
    fi
    
    echo -e "\n${GREEN}✅ Deployment complete: ${POLICY_ID}${NC}"
    echo -e "  Active: $ACTIVE_LINK → ${POLICY_ID}"
}

rollback() {
    echo -e "\n${YELLOW}========================================${NC}"
    echo -e "${YELLOW}  Rolling Back to Previous Policy${NC}"
    echo -e "${YELLOW}========================================${NC}\n"
    
    if [ ! -L "$BACKUP_DIR/previous" ]; then
        echo -e "${RED}❌ No backup found${NC}"
        exit 1
    fi
    
    BACKUP_PATH=$(readlink -f "$BACKUP_DIR/previous")
    BACKUP_ID=$(basename "$BACKUP_PATH")
    
    echo -e "  Rolling back to: ${GREEN}$BACKUP_ID${NC}"
    
    # 현재 active → 새 backup
    if [ -L "$ACTIVE_LINK" ]; then
        CURRENT=$(readlink -f "$ACTIVE_LINK")
        CURRENT_ID=$(basename "$CURRENT")
        ln -sfn "$CURRENT" "${BACKUP_DIR}/failed_${CURRENT_ID}"
        echo -e "  ${YELLOW}📦${NC} Current '$CURRENT_ID' saved as failed"
    fi
    
    # backup → active
    ln -sfn "$BACKUP_PATH" "$ACTIVE_LINK"
    
    echo -e "  ${GREEN}✅${NC} Rollback complete: $BACKUP_ID"
    
    # 서비스 재시작
    if systemctl is-active --quiet turtlebot3-policy 2>/dev/null; then
        sudo systemctl restart turtlebot3-policy
    fi
}

# ========== Main ==========
case "${1:-}" in
    --status|-s)
        status
        ;;
    --rollback|-r)
        rollback
        ;;
    --help|-h)
        echo "Usage:"
        echo "  bash scripts/deploy_policy.sh <model.plan> [policy_id]"
        echo "  bash scripts/deploy_policy.sh --rollback"
        echo "  bash scripts/deploy_policy.sh --status"
        echo "  bash scripts/deploy_policy.sh --help"
        ;;
    *)
        if [ -z "${1:-}" ]; then
            status
        else
            deploy "$1" "${2:-}"
        fi
        ;;
esac
