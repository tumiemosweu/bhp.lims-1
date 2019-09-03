# How to create a Sample with JSON.API

## Preliminaries

You can install RESTClient Add-on for Firefox for GET/POST requests simulations:
https://addons.mozilla.org/en-US/firefox/addon/restclient/

To beautify the JSON results, you might install JSON Lite for Firefox:
https://addons.mozilla.org/en-US/firefox/addon/json-lite/?src=recommended

`senaite.jsonapi` was developed using `plone.jsonapi.routes` as a reference. Thus, is strongly recommended to read the documentation for `plone.jsonapi.routes`, cause `senaite.jsonapi` works mostly the same way: https://plonejsonapiroutes.readthedocs.io/en/latest/

## Step-by-step guide (with example)

### Login to the system with a user with enough privileges

http://localhost:8080/senaite/http://localhost:8080/senaite/@@API/senaite/v1/login?__ac_name=user&__ac_password=secret

### Gather the information required:

#### Available (and active) Clients:

http://localhost:8080/senaite/@@API/senaite/v1/search?portal_type=Client&review_state=active

fine-grained search for clients (by name) can be done too:

http://localhost:8080/senaite/@@API/senaite/v1/search?portal_type=Client&review_state=active&Title=Ambition

From the list of clients, pick the unique identifier (param "uid") of the desired client

E.g: uid of "Ambition" client: `38e444dff19e4c4c93ce401666ddd36d`

#### Get the Client contact the Sample will be assigned to

Now, get the available contacts from the selected client (use the client's uid as value for "getParentUID" param):

http://localhost:8080/senaite/@@API/senaite/v1/search?portal_type=Contact&getParentUID=38e444dff19e4c4c93ce401666ddd36d

You can also search by username or any other index:

http://localhost:8080/senaite/@@API/senaite/v1/search?portal_type=Contact&getParentUID=38e444dff19e4c4c93ce401666ddd36d&getUsername=jjarvis

From the list of contacts, pick the uid of the desired contact

E.g uid of "Joe Jarvis": `ce0958f7162149e486570bc6ac695538`


#### Get the Analysis Templates available for this client

http://localhost:8080/senaite/@@API/senaite/v1/search?portal_type=ARTemplate&catalog=bika_setup_catalog&inactive_state=active&getClientUID=38e444dff19e4c4c93ce401666ddd36d

You can also search by title:

http://localhost:8080/senaite/@@API/senaite/v1/search?portal_type=ARTemplate&catalog=bika_setup_catalog&inactive_state=active&getClientUID=38e444dff19e4c4c93ce401666ddd36d&Title=blood

Pick the "uid", "getSampleTypeUID" from the desired Template
E.g:

- uid of "Complete Blood Count (CBC)": `59b525f060164edf94f1334748f81d1d`
- Sample Type uid of "Complete Blood Count (CBC)": `f2f039f6920645318e53dd160a3f9642`

#### Get the Sample Type

If you do a search a Sample Type by the uid you got in the previous step, you'll notice the Sample Type associated to the Template is "Whole Blood EDTA":

http://localhost:8080/senaite/@@API/senaite/v1/search?UID=f2f039f6920645318e53dd160a3f9642

If the Template has no sample type defined (or don't want to use a template), you can look for available (and active) Sample Types as follows:

http://localhost:8080/senaite/@@API/senaite/v1/search?portal_type=SampleType&inactive_state=active

A fine-grained search can be accomplished with additional params in the request:

http://localhost:8080/senaite/@@API/senaite/v1/search?portal_type=SampleType&inactive_state=active&title=Whole%20Blood%20EDTA


#### Get the Default Container Type

Get the full sample type object (param "complete"):

http://localhost:8080/senaite/@@API/senaite/v1/search?UID=f2f039f6920645318e53dd160a3f9642&complete=True

From the response, extract the container type uid (["ContainerType"]["uid"):

E.g. `b54ac1bccffb46fd8598e862e6be087f`

If you do a search for this UID you'll see that the container type is "EDTA Tube":

http://localhost:8080/senaite/@@API/senaite/v1/containertype/b54ac1bccffb46fd8598e862e6be087f

### Sample creation via POST

At this point, we have almost all the information we need for the creation of a Sample:

The create action in `json.api` must be done with a **POST request** to:

http://localhost:8080/senaite/@@API/senaite/v1/AnalysisRequest/create/<client_uid>

Where `<client_uid>` is the UID of the client we got before. In this example, the url should look like:

http://localhost:8080/senaite/@@API/senaite/v1/AnalysisRequest/create/38e444dff19e4c4c93ce401666ddd36d

Then, the information provided via POST should look similar to:

```
{"SampleType": <sample_type_uid>,
 "Contact": <contact_uid>,
 "Template": <template_uid>,
 "DateSampled": "",
 "ParticipantID": "",
 "OtherParticipantReference": "",
 "ParticipantInitials": "",
 "Gender": "m",
 "Visit": "", 
 "DateOfBirth": "",
 "Fasting": False,
 "ClientSampleID": "",
 "Volume": "",
 "DefaultContainerType": <container_type_uid>,
 "OtherInformation": "",
 "Priority": 3,
 "Remarks": ""}
```

Note that values for at least mandatory fields ("ParticipantID", "DateSampled", etc.) must be set.
