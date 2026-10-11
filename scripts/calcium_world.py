import json
import boto3
from botocore.exceptions import ClientError

# 1. Prepare the JSON Metadata Payload
payload = {
    "document_id": "doc_muscle_skin_contraction_001",
    "metadata": {
        "title": "What Happens When You Contract a Muscle or Skin Area",
        "content_type": "educational_article",
        "domain": "human_physiology",
        "topics": [
            "nervous_system",
            "neuromuscular_junction",
            "sliding_filament_theory",
            "smooth_muscle",
            "skeletal_muscle"
        ],
        "sources": [
            {"name": "scienceinsights.org", "citation_count": 5},
            {"name": "Wikipedia", "citation_count": 1},
            {"name": "Visible Body", "citation_count": 1}
        ],
        "created_at": "2026-10-05T09:26:00Z",
        "language": "en-US"
    },
    "content": {
        "summary": "Contracting a muscle or skin area involves nerve-triggered electrical signals, acetylcholine release, calcium ions exposing actin binding sites, and myosin sliding filaments to shorten tissue until the signal ends.",
        "key_takeaways": [
            "Muscle contraction is a rapid sequence involving nerve electricity, calcium, and protein sliding.",
            "Skin contraction involves underlying smooth muscle or arrector pili activity rather than the epidermis.",
            "The entire process takes only milliseconds in skeletal muscle."
        ],
        "sequential_steps": [
            {
                "step_number": 1,
                "name": "Nerve Signal Initiation",
                "description": "Brain or spinal cord sends an electrical impulse down a motor neuron to target tissue."
            },
            {
                "step_number": 2,
                "name": "Chemical Trigger at Neuromuscular Junction",
                "description": "Acetylcholine is released into the synaptic gap, binding to receptors and letting sodium rush into muscle cells."
            },
            {
                "step_number": 3,
                "name": "Calcium Release & Protein Interaction",
                "description": "Impulse triggers sarcoplasmic reticulum to release calcium, exposing actin binding sites."
            },
            {
                "step_number": 4,
                "name": "Sliding Filament Mechanism",
                "description": "Myosin heads pull actin filaments toward the center of the sarcomere, shortening the muscle fiber."
            },
            {
                "step_number": 5,
                "name": "Relaxation",
                "description": "Nerve signal ceases, calcium is pumped back, and muscle returns to resting length."
            }
        ]
    }
}


def send_to_cloud(data_dict: dict, bucket_name: str, object_key: str):
    """Serializes JSON dictionary and uploads directly to AWS S3."""
    s3_client = boto3.client('s3')
    json_bytes = json.dumps(data_dict, indent=2).encode('utf-8')
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json_bytes,
            ContentType='application/json'
        )
        print(f" Successfully uploaded payload to s3://{bucket_name}/{object_key}")
    except ClientError as e:
        print(f" Error uploading to S3: {e}")


def retrieve_from_cloud(bucket_name: str, object_key: str) -> dict:
    """Retrieves JSON object from AWS S3 and parses it back to a Python dictionary."""
    s3_client = boto3.client('s3')
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        content_str = response['Body'].read().decode('utf-8')
        retrieved_data = json.loads(content_str)
        print(f" Successfully retrieved payload from s3://{bucket_name}/{object_key}")
        return retrieved_data
    except ClientError as e:
        print(f" Error downloading from S3: {e}")
        return {}


# --- Execution Example ---
if __name__ == "__main__":
    BUCKET_NAME = "my-educational-metadata-bucket"
    OBJECT_KEY = "physiology/doc_muscle_skin_contraction_001.json"

    # 1. Upload to Cloud
    send_to_cloud(payload, BUCKET_NAME, OBJECT_KEY)

    # 2. Retrieve back down from Cloud
    retrieved_json = retrieve_from_cloud(BUCKET_NAME, OBJECT_KEY)

    # Output retrieved summary to confirm match
    if retrieved_json:
        print("\nRetrieved Summary from Cloud:")
        print(retrieved_json["content"]["summary"])
