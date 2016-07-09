# SPEER

# Depdendencies

* Python 3
* Virtualenv
* Bash

# Installation

    # Get source
    git clone git@github.com:JonasGroeger/SPEER.git
    cd SPEER
    
    # Create virtualenv
    virtualenv venv # Assuming Python3
    source venv/bin/activate
    
    # Install dependencies into virtualenv
    pip install -r requirements.txt
    
# Starting the whole thing

    # This Terminal: Publishers
    ./start_publishers
    
    # New Terminal: Subscribers
    cd SPEER
    source venv/bin/activate
    ./start_subscribers
    
    # New Terminal: Brokers
    cd SPEER
    source venv/bin/activate
    ./start_brokers

# Stopping the whole thing

Since the shell scripts start the processes in the background (publishers, brokers), there is a kill script that kills **ALL** Python 3 processes called killall-python3`. Only run this if you know what you are doing.

    ./killall-python3
    
# License

MIT License

Copyright (c) 2016 Jonas Gröger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
