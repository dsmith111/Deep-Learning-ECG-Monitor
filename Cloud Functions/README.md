# Cloud Functions

These folders represent the source code that would be used directly in GCP cloud functions.

## Descriptions

- process-classify
  - This cloud function is triggered whenever a change occurs within Cloud Storage. If the data is not of a csv type or not within a specified bucket, the event is ignored. Otherwise, the function follows this path:
    - Data is processed in a model friendly format
    - Model is loaded from Cloud Storage
    - Inference is made
    - Result is forwarded to a separate REST cloud function for decision handling.
- alert-user
  - This REST based cloud function takes the result from the classifier and if the result is abnormal, it connects with the Twilio API to alert the user.
