from uuid import uuid4
import os
import yaml
import coloredlogs
from flask import Flask, jsonify
import logging
import logging.config
from pychain.blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace("-", "")

# Instantiate the Blockchain
blockchain = Blockchain()


# Instantiate Logger
def setup_logging(
    default_path="../res/logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"
):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print("Error in Logging Configuration. Using default configs")
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print("Failed to load configuration file. Using default configs")


@app.route("/mine", methods=["GET"])
def mine():
    return "We'll mine a new Block"


@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    return "We'll add a new transaction"


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain),
    }
    return jsonify(response), 200


if __name__ == "__main__":
    setup_logging()
    app.run(host="0.0.0.0", port=5000)
