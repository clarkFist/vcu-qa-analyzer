#!/bin/bash

###############################################################################
# 快速项目分析脚本
# 用法: ./quick_analyze.sh [项目路径] [选项]
###############################################################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 默认值
PROJECT_PATH="${1:-.}"
OUTPUT_FORMAT="${2:-html}"
OUTPUT_NAME="${3:-analysis_report}"

# 帮助信息
show_help() {
    cat << EOF
${BLUE}项目分析工具 - 快速启动脚本${NC}

用法:
    $0 [项目路径] [格式] [输出名称]

参数:
    项目路径    要分析的项目目录 (默认: 当前目录)
    格式        输出格式: html, markdown, both (默认: html)
    输出名称    输出文件名 (默认: analysis_report)

示例:
    # 分析当前项目
    $0

    # 分析指定项目
    $0 ~/projects/my-app

    # 生成 Markdown 报告
    $0 ~/projects/my-app markdown

    # 自定义输出名称
    $0 ~/projects/my-app html my_custom_report

    # 分析多个项目
    $0 ~/projects/app1 html app1_report
    $0 ~/projects/app2 html app2_report
    $0 ~/projects/app3 html app3_report

选项:
    -h, --help      显示此帮助信息
    -v, --verbose   详细输出模式
    -l, --list      列出常见项目位置

环境变量:
    ANALYZER_OUTPUT_DIR    默认输出目录 (默认: 当前目录)

EOF
}

# 列出常见项目位置
list_projects() {
    echo -e "${BLUE}常见项目位置:${NC}\n"

    # 检查常见的项目目录
    COMMON_DIRS=(
        "$HOME/projects"
        "$HOME/work"
        "$HOME/dev"
        "$HOME/Documents/projects"
        "$HOME/Desktop"
    )

    for dir in "${COMMON_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            echo -e "${GREEN}✓${NC} $dir"
            # 列出子目录
            if [ "$(ls -A "$dir" 2>/dev/null)" ]; then
                ls -1 "$dir" | head -5 | sed 's/^/  - /'
                count=$(ls -1 "$dir" | wc -l)
                if [ "$count" -gt 5 ]; then
                    echo "  ... 还有 $((count - 5)) 个项目"
                fi
            fi
            echo
        fi
    done
}

# 检查参数
case "$1" in
    -h|--help)
        show_help
        exit 0
        ;;
    -l|--list)
        list_projects
        exit 0
        ;;
    -v|--verbose)
        VERBOSE="-v"
        PROJECT_PATH="${2:-.}"
        OUTPUT_FORMAT="${3:-html}"
        OUTPUT_NAME="${4:-analysis_report}"
        ;;
esac

# 验证项目路径
if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}❌ 错误: 项目路径不存在: $PROJECT_PATH${NC}"
    echo -e "${YELLOW}💡 提示: 使用 '$0 --list' 查看常见项目位置${NC}"
    exit 1
fi

# 转换为绝对路径
PROJECT_PATH="$(cd "$PROJECT_PATH" && pwd)"
PROJECT_NAME="$(basename "$PROJECT_PATH")"

# 确定输出目录
OUTPUT_DIR="${ANALYZER_OUTPUT_DIR:-$PWD}"
OUTPUT_PATH="$OUTPUT_DIR/$OUTPUT_NAME"

# 显示分析信息
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📊 项目分析工具${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}项目名称:${NC} $PROJECT_NAME"
echo -e "${GREEN}项目路径:${NC} $PROJECT_PATH"
echo -e "${GREEN}输出格式:${NC} $OUTPUT_FORMAT"
echo -e "${GREEN}输出路径:${NC} $OUTPUT_PATH"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# 检查 Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到 Python${NC}"
    exit 1
fi

# 检查依赖
echo -e "${YELLOW}🔍 检查依赖...${NC}"
if ! python -c "import markdown" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  警告: 缺少 markdown 库，尝试安装...${NC}"
    pip install markdown Pygments -q || {
        echo -e "${RED}❌ 依赖安装失败，请手动运行: pip install -r requirements.txt${NC}"
        exit 1
    }
fi

# 运行分析
echo -e "${GREEN}🚀 开始分析...${NC}\n"

cd "$SCRIPT_DIR"

python analyze_project.py \
    "$PROJECT_PATH" \
    -o "$OUTPUT_PATH" \
    -f "$OUTPUT_FORMAT" \
    ${VERBOSE:-}

# 检查结果
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ 分析完成！${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

    # 显示生成的文件
    echo -e "${BLUE}📄 生成的报告:${NC}"
    case "$OUTPUT_FORMAT" in
        html)
            echo -e "  ${GREEN}HTML:${NC} $OUTPUT_PATH.html"
            ;;
        markdown)
            echo -e "  ${GREEN}Markdown:${NC} $OUTPUT_PATH.md"
            ;;
        both)
            echo -e "  ${GREEN}HTML:${NC} $OUTPUT_PATH.html"
            echo -e "  ${GREEN}Markdown:${NC} $OUTPUT_PATH.md"
            ;;
    esac

    # 提取评分（如果是 markdown 格式）
    if [ -f "$OUTPUT_PATH.md" ]; then
        SCORE=$(grep "综合评分" "$OUTPUT_PATH.md" | grep -oE '[0-9]+' | head -1 || echo "N/A")
        GRADE=$(grep "综合评分" "$OUTPUT_PATH.md" | grep -oE '\([A-F]\)' | tr -d '()' || echo "N/A")

        echo -e "\n${BLUE}📊 项目评分:${NC}"
        echo -e "  ${GREEN}分数:${NC} $SCORE/100"
        echo -e "  ${GREEN}等级:${NC} $GRADE"

        # 根据评分显示建议
        if [ "$SCORE" != "N/A" ] && [ "$SCORE" -lt 60 ]; then
            echo -e "\n${YELLOW}⚠️  项目质量需要改进${NC}"
        elif [ "$SCORE" != "N/A" ] && [ "$SCORE" -ge 80 ]; then
            echo -e "\n${GREEN}🎉 项目质量良好！${NC}"
        fi
    fi

    # 打开报告（可选）
    if [ "$OUTPUT_FORMAT" = "html" ] || [ "$OUTPUT_FORMAT" = "both" ]; then
        echo -e "\n${YELLOW}💡 提示: 使用浏览器打开 HTML 文件查看完整报告${NC}"

        # 询问是否打开
        read -p "是否现在打开报告? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if command -v open &> /dev/null; then
                open "$OUTPUT_PATH.html"
            elif command -v xdg-open &> /dev/null; then
                xdg-open "$OUTPUT_PATH.html"
            else
                echo -e "${YELLOW}⚠️  无法自动打开，请手动打开: $OUTPUT_PATH.html${NC}"
            fi
        fi
    fi

    echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
else
    echo -e "\n${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}❌ 分析失败${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}💡 提示: 使用 '$0 -v' 查看详细错误信息${NC}"
    exit 1
fi
