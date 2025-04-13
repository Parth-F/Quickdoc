#!/bin/bash

# Default values
MODEL_PATH="/home/parth/QuickDoc/Models/model.gguf"
PROMPT="What is your name?"
NUM_TOKENS=128
INTERACTIVE=false
TEMPERATURE=0.7
CTX_SIZE=8192

# Help function
show_help() {
    echo "Usage: ./run_model.sh [OPTIONS]"
    echo "Run the GGUF model with custom parameters"
    echo ""
    echo "Options:"
    echo "  -p, --prompt STRING       Prompt to send to the model (default: \"$PROMPT\")"
    echo "  -n, --tokens NUMBER       Number of tokens to generate (default: $NUM_TOKENS)"
    echo "  -i, --interactive         Run in interactive mode"
    echo "  -t, --temp FLOAT          Temperature setting (default: $TEMPERATURE)"
    echo "  -c, --ctx NUMBER          Context size (default: $CTX_SIZE)"
    echo "  -h, --help                Show this help message"
    echo ""
    echo "Example: ./run_model.sh -p \"Tell me about diabetes\" -n 512"
    echo "Example: ./run_model.sh -i"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--prompt)
            PROMPT="$2"
            shift 2
            ;;
        -n|--tokens)
            NUM_TOKENS="$2"
            shift 2
            ;;
        -i|--interactive)
            INTERACTIVE=true
            shift
            ;;
        -t|--temp)
            TEMPERATURE="$2"
            shift 2
            ;;
        -c|--ctx)
            CTX_SIZE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Build the command
CMD="cd /home/parth/QuickDoc/llama.cpp && ./bin/llama-cli -m $MODEL_PATH --ctx-size $CTX_SIZE --temp $TEMPERATURE"

if [ "$INTERACTIVE" = true ]; then
    CMD="$CMD -i"
else
    CMD="$CMD -n $NUM_TOKENS -p \"$PROMPT\""
fi

# Run the command
echo "Running model with command:"
echo "$CMD"
echo "------------------------------"
eval $CMD
