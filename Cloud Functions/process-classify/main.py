def Convert_Function(event, context):
    """Triggered by a change to a Cloud Storage bucket.
   Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
   """

    import pandas as pd
    import numpy as np
    try:
        import keras
    except:
        from tensorflow import keras
    import requests

    # Log event detalis
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))

    # Only accept CSV uploads
    if ("csv" not in event["name"]) or (event['bucket'] != "ECG_BUCKET"):
        return

    def convert_ecg(df: pd.DataFrame):
        signals = np.asarray([signal for index, signal in df.iterrows()])
        return signals

    bucketName = event['bucket']
    blobName = event['name']
    fileName = "gs://" + bucketName + "/" + blobName
    ecg_df = pd.read_csv(fileName)
    records = convert_ecg(ecg_df)

    # Load model based on Keras loaded
    print("loading model")
    try:
        model = keras.model.load(
            "gs://" + "PATH_TO_AI_MODEL" + "classifier.h5")
    except:
        model = keras.models.load_model(
            "gs://" + "PATH_TO_AI_MODEL" + "classifier.h5")
    labels = {
        0: "Normal",
        1: "SVEB",
        2: "VEB",
        3: "Fusion",
        4: "Unknown"
    }

    print("running model")
    pred = model.predict(records)
    pred_label = labels[list(pred[0]).index(max(pred[0]))]
    url = "https://REGION-PROJECT-NAME.cloudfunctions.net/FUNCTION?key=GCP_KEY"
    headers = {
        "Content-Type": "application/json",
    }
    body = {
        "message": pred_label
    }
    print("Posting results")
    post_request = requests.post(headers=headers, url=url, json=body)

    return{
        "statusCode": 200,
        "body": "success"
    }
