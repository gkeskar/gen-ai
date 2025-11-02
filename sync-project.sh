#!/bin/bash

# Sync Project Script
# Copies projects from the course repo (agents) to this repo (gen-ai)

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Paths
COURSE_REPO="/Users/gkeskar/projects/agents"
GEN_AI_REPO="/Users/gkeskar/projects/gen-ai"

echo -e "${BLUE}📦 Gen-AI Project Sync Tool${NC}"
echo ""

# Check if project name provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: No project name provided${NC}"
    echo ""
    echo "Usage: ./sync-project.sh <project_name>"
    echo ""
    echo "Available projects:"
    echo "  - code_learning_assistant"
    echo ""
    exit 1
fi

PROJECT=$1

case $PROJECT in
    code_learning_assistant|code-assistant)
        echo -e "${BLUE}Syncing Code Learning Assistant...${NC}"
        SOURCE="$COURSE_REPO/2_openai/code_learning_assistant/code-assistant"
        DEST="$GEN_AI_REPO/code-assistant"
        
        if [ ! -d "$SOURCE" ]; then
            echo -e "${RED}❌ Source directory not found: $SOURCE${NC}"
            exit 1
        fi
        
        echo "  Source: $SOURCE"
        echo "  Dest:   $DEST"
        echo ""
        
        # Create destination if it doesn't exist
        mkdir -p "$DEST"
        
        # Copy files (excluding certain patterns)
        rsync -av --delete \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='.git' \
            --exclude='.env' \
            --exclude='learning_docs' \
            --exclude='.DS_Store' \
            "$SOURCE/" "$DEST/"
        
        echo ""
        echo -e "${GREEN}✅ Code Learning Assistant synced successfully!${NC}"
        ;;
        
    *)
        echo -e "${RED}❌ Unknown project: $PROJECT${NC}"
        echo ""
        echo "Available projects:"
        echo "  - code_learning_assistant"
        echo ""
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "  cd $GEN_AI_REPO"
echo "  git status                  # Review changes"
echo "  git add ."
echo "  git commit -m 'Update $PROJECT'"
echo "  git push origin main"
echo ""

