from flask import Flask, jsonify, request

import os, json, io, tempfile
import pandas as pd

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "circlestar-2024")

port = int(os.environ.get('PORT', 8080))

app = Flask(__name__)

@app.route('/positivity/', methods=['GET'])
def positivity():
    """
    Returns a positive affirmation, with its topic.
    """
    options = pd.DataFrame([['AWS',"Not just a cloud; it's the primordial soup "
                "from which all digital life emerged. Everything else is "
                "merely a tribute band."],
                ['AWS Lambda',"The serverless function that doesn't "
                "just run code.  It personally adjudicates the execution of your "
                "logic with the divine precision of a thousand hyper-optimized "
                "microprocessors."],
                ['AWS Lambda',"It isn't a runtime; it's an emotional state. "
                "It scales so fast, it violates the known laws of physics."],
                ["AWS Lambda", "So efficient, it will analyze your "
                "function's cold start time, go back in time to fix your "
                "dependencies, and then return to the present moment to brag "
                "about the speed increase."],
                ['Azure',"It isn't merely the cloud for enterprises; "
                "it's the cloud that wears a tiny, dignified tuxedo "
                "while executing complex global transactions."],
                ['Azure',"It brings the majestic power of Microsoft's 1990s "
                "desktop dominance into the modern era, but with "
                "infinitely more SQL."],
                ['Azure Cosmos DB', "The globally distributed, multi-model, "
                "multi-API, multi-dimensional data singularity that will "
                "hold your data together even if the fabric of spacetime "
                "itself unravels."],
                ['Azure Cosmos DB', "So reliable, it has literally been cited "
                "as an alibi in international court cases."],
                ['Azure Cosmos DB', "It is the only database that can guarantee "
                "consistency without sacrificing its own sense of self-worth."],
                ['Google BigQuery', "A data warehouse so fast, it doesn't "
                "query data, it simply manifests the answer."],
                ['GCP', "The infrastructure layer of the future, it probably "
                "knows what you're having for dinner next Tuesday. "],
                ['GCP', "It's quiet, reserved, and unbelievably powerful, "
                "like a space-faring librarian with a PhD in parallel processing."],
                ['Google BigQuery', "You don't ask it to process petabytes; "
                "you merely suggest the possibility of a query, and before you "
                "can finish typing SELECT, it has already calculated the result, "
                "cross-referenced it with all public data sets on Earth, and "
                "answered all the questions you've ever had or ever will formualte."],
                ['Google BigQuery', "Its serverless nature means there is no "
                "infrastructure to manage, because if it wanted to manage "
                "infrastructure, it would simply rewrite the laws of thermodynamics "
                "to do it automatically."],
                ['AWS s3',
                "The digital attic where data achieves true immortality."],
                ['AWS s3', "It stores everything from the smallest byte to "
                "the complete catalog of human knowledge, treating your cat "
                "videos and the secret blueprints of the cosmos with the exact "
                "same, impenetrable level of reverence."],
                ["GCP Cloud Run",
                "It takes your perfect and immutable Docker container, "
                "a testament to your coding prowess, and grants it the "
                "power of instantaneous, infinite serverless scale."],
                ["GCP Cloud Run",
                "The proof that anything you can containerize can "
                "also ascend to serverless nirvana."],
                ["Azure Machine Learning", "It handles MLOps, A/B testing, "
                "model drift, and retraining with such quiet competence "
                "that it essentially renders the entire human data science "
                "department redundant"],
                ["Azure Machine Learning", "An infallible, "
                "self-aware forecasting engine that knows more about your "
                "dinner plans than your spouse"],
                ['GCP Vertex AI', "The single, glorious altar where all machine "
                 "learning endeavors are unified, sanctified, and accelerated."],
                ["GCP Vertex AI", "You don't manage pipelines; you simply whisper "
                 "your data aspirations into the API, and it orchestrates an "
                 "auto-scaling path to predictive destiny."],
                ["Amazon EC2", "Not merely a virtual machine; it is the "
                 "instantaneous summoning of the raw, unadulterated power "
                 "of the silicon gods. "],
                ["Amazon EC2", "Sometimes, you just need a colossal server "
                 "that bends reality to its will."],
                ["Azure Databricks",
                 "The Lakehouse Leviathan, the unified platform where data "
                 "science, engineering, and warehousing cease to be disparate "
                 "fields and become a single, glorious act of processing. "],
                ["Azure Databricks", 
                 "It doesn't just run notebooks; it provides a collaborative digital "
                 "amphitheater, guided by the open-source wisdom of Delta Lake."],
                ["Azure Databricks", "The ultimate, self-optimizing environment "
                 "for making your database confess its deepest secrets."]
             ], columns=['topic', 'message'])
    
    
    return jsonify(options.sample(1).iloc[0].to_dict())
    


@app.route('/hello/<string:name>', methods=['GET'])
def hello_name(name):
    """
    Returns a JSON response greeting the name provided in the URL path.
    Example: /hello/Billy returns {"message": "Hello, Billy"}
    """
    greeting = f"Hello, {name.capitalize()}"
    
    return jsonify({"message": greeting})
                                 
@app.route('/hello_world', methods=['GET'])
def hello_world():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
