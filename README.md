# Net-Topo-Drawer

Net-Topo-Drawer is a two-person project designed to automatically display network topology. The project consists of two main components: a crawler that collects network data with the use of LLDP protocol and a graphical interface that automatically draws the network topology based on the information from the crawler.
The application was tested in [GNS3](https://www.gns3.com/) environment only.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.8 or higher
- pip (Python package installer)
- Git
- netmiko, netgraph, tkinter, matplotlib, numpy, networkx

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/net-topo-drawer.git
    cd net-topo-drawer
    ```

2. Install the required Python packages.

## Usage

### Running the app

To run the app use the following command:

```sh
python main.py
```

## Features

- **Real-time Network Topology Visualization:** Automatically updates the network topology based on live data from the crawler.
- **User-Friendly Interface:** Easy-to-use graphical interface to view network topology.
- **Modularity:** Crawler and graphical interface are modular, allowing for easy updates and maintenance.

Thank you for using Net-Topo-Drawer! We hope it helps you visualize and manage your network topology effectively :)
