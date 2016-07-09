# SPEER

# Installation

    # Get source
    git clone git@github.com:JonasGroeger/SPEER.git
    cd SPEER
    
    # Create virtualenv
    virtualenv venv # Assuming Python3
    source venv/bin/activate
    
    # Install dependencies into virtualenv
    pip install -r requirements.txt
    
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
