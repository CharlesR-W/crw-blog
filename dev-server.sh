#!/bin/bash

# Jekyll Development Server Script
# Usage: ./dev-server.sh [start|stop|restart|status]

BLOG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$BLOG_DIR/jekyll.pid"
LOG_FILE="$BLOG_DIR/jekyll.log"

case "$1" in
    start)
        echo "Starting Jekyll development server..."
        cd "$BLOG_DIR"
        # Start Jekyll in background and capture PID
        bundle exec jekyll serve --host 0.0.0.0 --port 4000 --detach > "$LOG_FILE" 2>&1 &
        JEKILL_PID=$!
        echo $JEKILL_PID > "$PID_FILE"
        sleep 2
        if kill -0 $JEKILL_PID 2>/dev/null; then
            echo "✅ Server started successfully!"
            echo "🌐 Access your blog at: http://localhost:4000/crw-blog/"
            echo "📝 Log file: $LOG_FILE"
            echo "🆔 PID file: $PID_FILE"
        else
            echo "❌ Failed to start server. Check log file: $LOG_FILE"
            rm -f "$PID_FILE"
        fi
        ;;
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            echo "Stopping Jekyll server (PID: $PID)..."
            kill "$PID" 2>/dev/null
            rm -f "$PID_FILE"
            echo "✅ Server stopped."
        else
            echo "❌ No PID file found. Server may not be running."
        fi
        ;;
    restart)
        echo "Restarting Jekyll server..."
        "$0" stop
        sleep 2
        "$0" start
        ;;
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "✅ Jekyll server is running (PID: $PID)"
                echo "🌐 URL: http://localhost:4000/crw-blog/"
            else
                echo "❌ Server PID file exists but process is not running"
                rm -f "$PID_FILE"
            fi
        else
            echo "❌ Jekyll server is not running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the Jekyll development server"
        echo "  stop    - Stop the Jekyll development server"
        echo "  restart - Restart the Jekyll development server"
        echo "  status  - Check if the server is running"
        exit 1
        ;;
esac 