#!/bin/bash

# Dynamic Traffic Signal AI - Quick Launcher

clear
echo "============================================================"
echo "   Dynamic Traffic Signal AI - Quick Launcher"
echo "============================================================"
echo ""
echo "Choose an option:"
echo ""
echo "[1] Dashboard Only (No Arduino)"
echo "[2] Arduino Controller Only"
echo "[3] Full System (Arduino + Dashboard)"
echo "[4] Test Synchronization"
echo "[5] Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Starting Dashboard Only..."
        echo "Open your browser to: http://localhost:5000"
        echo "Press Ctrl+C to stop"
        echo ""
        cd dashboard
        python3 app.py
        ;;
    2)
        echo ""
        echo "Starting Arduino Controller..."
        echo "Make sure Arduino is connected!"
        echo "Press Ctrl+C to stop"
        echo ""
        cd src
        python3 main.py
        ;;
    3)
        echo ""
        echo "Starting Full System..."
        echo ""
        echo "This will open 2 terminal windows:"
        echo "  1. Arduino Controller"
        echo "  2. Web Dashboard"
        echo ""
        echo "Then open your browser to: http://localhost:5000"
        echo ""
        read -p "Press Enter to continue..."
        
        # Start Arduino controller in new terminal
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd src && python3 main.py; exec bash"
            sleep 2
            gnome-terminal -- bash -c "cd dashboard && python3 app.py; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd src && python3 main.py" &
            sleep 2
            xterm -e "cd dashboard && python3 app.py" &
        else
            echo "Please open 2 terminals manually and run:"
            echo "  Terminal 1: cd src && python3 main.py"
            echo "  Terminal 2: cd dashboard && python3 app.py"
        fi
        
        echo ""
        echo "Both systems started!"
        read -p "Press Enter to exit..."
        ;;
    4)
        echo ""
        echo "Running synchronization test..."
        echo ""
        python3 test_sync.py
        echo ""
        read -p "Press Enter to continue..."
        ;;
    5)
        echo ""
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo ""
        echo "Invalid choice!"
        read -p "Press Enter to exit..."
        ;;
esac
