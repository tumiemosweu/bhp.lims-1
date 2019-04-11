# Releases

## 190411 (19-04-11)

- `bhp.lims` [@cdf206d](https://github.com/bhp-lims/bhp.lims/tree/cdf206d4b26c1cf199f6d5bff9700116b8626083)
- `senaite.api` v1.2.3-r2 [@c79c53a](https://github.com/senaite/senaite.api/tree/c79c53abcbe6e3a5ab3ced86d2f455275efa20cf)
- `senaite.core` v1.3.1 [@77177d3](https://github.com/senaite/senaite.core/tree/77177d3c4e9c3ba7e1fa1b8869a24a5b427dcd92)
- `senaite.core.listing` v1.2.0 [@1a32bff](https://github.com/senaite/senaite.core.listing/tree/1a32bff1c8189b482cce9913df5348c7b242754b)
- `senaite.core.supermodel` v1.3.0 [@318921c](https://github.com/senaite/senaite.core.supermodel/tree/318921cba001994c9cafa6d2231623fb2b871627)
- `senaite.impress` v1.2.0 [@c958dbd](https://github.com/senaite/senaite.impress/tree/c958dbd194018cd063d02998b43b57fbf610b2aa)
- `senaite.jsonapi` v1.2.1 [@871959f](https://github.com/senaite/senaite.jsonapi/tree/871959f4b1c9edbb477e9456325527ca78e13ec6)
- `senaite.lims` v1.3.0 [@94f2a4a](https://github.com/senaite/senaite.lims/tree/94f2a4ae01c4fbce6182dc3ea281b128c908dccd)
- `senaite.storage` v1.0.0 [@3f5454f](https://github.com/senaite/senaite.storage/tree/3f5454f28ac2917d0c504492130f2a03c1fd256e)

### Deployment notes

Estimated time for update/deployment completion: 2h

- Upgrade `senaite.core` version 1.3.0
- Reinstall (QuickInstaller) `senaite.lims`
- Reinstall (QuickInstaller) `senaite.impress`
- Reinstall (QuickInstaller) `senaite.storage`
- Reinstall (QuickInstaller) `bhp.lims`

### Differences with production

- #227 Export filtered by client
- #167 Allow dropdown menu for volume units when creating an Analysis Request
- #223 Add client sample id in requisition form
- #215 Adding other choices visit code field
- #106 When adding new Analysis Request from clinic then upload an attachment ...
- #221 After creating more than one ar, not all analysis request's appear in next page ...
- #74 Value for Gender cannot be copied across columns in Analysis Request Add form
- [SC#1319](https://github.com/senaite/senaite.core/pull/1319) Fix AttributeError: state_variable
- [SC#1320](https://github.com/senaite/senaite.core/pull/1320) Make api.get_review_history to always return a list
- [SC#1318](https://github.com/senaite/senaite.core/pull/1318) Add function addAttachment in Sample to preserve previous attachments
- [SC#1317](https://github.com/senaite/senaite.core/pull/1317) Fix Analysis Service URL in Info Popup
- [SC#1312](https://github.com/senaite/senaite.core/pull/1312) Reject adapter does not consider analyses have reject action too
- [SC#1296](https://github.com/senaite/senaite.core/pull/1296) Setting the Price via "Manage Analyses" does not work and breaks the invoice calculation
- [SC#1303](https://github.com/senaite/senaite.core/pull/1303) Preserve review history in 1.3 upgrade
- [SC#1270](https://github.com/senaite/senaite.core/pull/1270) Log Tab of Client Sample Points rises Traceback
- [SC#1305](https://github.com/senaite/senaite.core/pull/1305) Ensure analyses from primary are removed after being added to partitions
- [SC#1304](https://github.com/senaite/senaite.core/pull/1304) Some Items show the Display/State/Add menu
- [SC#1307](https://github.com/senaite/senaite.core/pull/1307) Traceback when using «Submit» of the global WF menu
- [SC#1309](https://github.com/senaite/senaite.core/pull/1309) Added Samples rejection view
- [SC#1310](https://github.com/senaite/senaite.core/pull/1310) Support for radio copy in Sample Add view
- [SL#100](https://github.com/senaite/senaite.lims/pull/100) Improve Styling of Navigation Portlet
- [SI#67](https://github.com/senaite/senaite.impress/pull/67) Fix PublicationPreference Traceback in Default template

*SC: changes in `senaite.core` add-on*

*SL: changes in `senaite.lims` add-on*

*SI: changes in `senaite.impress` add-on*


## 190401 (19-04-01)

- `bhp.lims` [@3010260](https://github.com/bhp-lims/bhp.lims/tree/30102609d5c0a5bbd1c751846d5d77b919d56ab7)
- `senaite.api` v1.2.3-r2 [@c79c53a](https://github.com/senaite/senaite.api/tree/c79c53abcbe6e3a5ab3ced86d2f455275efa20cf)
- `senaite.core` v1.3.0 [@bfce6cc](https://github.com/senaite/senaite.core/tree/bfce6cc8feb31a02b612f9141d00d4106e33fcda)
- `senaite.core.listing` v1.2.0 [@1a32bff](https://github.com/senaite/senaite.core.listing/tree/1a32bff1c8189b482cce9913df5348c7b242754b)
- `senaite.core.supermodel` v1.3.0 [@318921c](https://github.com/senaite/senaite.core.supermodel/tree/318921cba001994c9cafa6d2231623fb2b871627)
- `senaite.impress` v1.2.0 [@2b339a1](https://github.com/senaite/senaite.impress/tree/2b339a12ff9ad3c78470d6660e97964ad0b89b26)
- `senaite.jsonapi` v1.2.1 [@871959f](https://github.com/senaite/senaite.jsonapi/tree/871959f4b1c9edbb477e9456325527ca78e13ec6)
- `senaite.lims` v1.3.0 [@5213265](https://github.com/senaite/senaite.lims/tree/5213265fb14e0f85fd97af0442d3ce44b7e57500)
- `senaite.storage` v1.0.0 [@3f5454f](https://github.com/senaite/senaite.storage/tree/3f5454f28ac2917d0c504492130f2a03c1fd256e)

### Deployment notes

Estimated time for update/deployment completion: 2h

- Upgrade `senaite.core` version 1.3
- Reinstall (QuickInstaller) `senaite.lims` 
- Reinstall (QuickInstaller) `senaite.impress`
- Reinstall (QuickInstaller) `senaite.storage` 
- Reinstall (QuickInstaller) `bhp.lims`

### Differences with production

- #74 Value for Gender cannot be copied across columns in Analysis Request Add form
- [SC#1296](https://github.com/senaite/senaite.core/pull/1296) Setting the Price via "Manage Analyses" does not work and breaks the invoice calculation
- [SC#1303](https://github.com/senaite/senaite.core/pull/1303) Preserve review history in 1.3 upgrade
- [SC#1270](https://github.com/senaite/senaite.core/pull/1270) Log Tab of Client Sample Points rises Traceback
- [SC#1305](https://github.com/senaite/senaite.core/pull/1305) Ensure analyses from primary are removed after being added to partitions
- [SC#1304](https://github.com/senaite/senaite.core/pull/1304) Some Items show the Display/State/Add menu
- [SC#1307](https://github.com/senaite/senaite.core/pull/1307) Traceback when using «Submit» of the global WF menu
- [SC#1309](https://github.com/senaite/senaite.core/pull/1309) Added Samples rejection view
- [SC#1310](https://github.com/senaite/senaite.core/pull/1310) Support for radio copy in Sample Add view
- [SL#100](https://github.com/senaite/senaite.lims/pull/100) Improve Styling of Navigation Portlet

*SC: changes in `senaite.core` add-on*
*SL: changes in `senaite.lims` add-on*


## 190320 (19-03-20)

- `bhp.lims` [@68cca07](https://github.com/bhp-lims/bhp.lims/tree/68cca076fbe999f2c6465e4c6a43790d0c5593e3)
- `senaite.api` [@c79c53a](https://github.com/senaite/senaite.api/tree/c79c53abcbe6e3a5ab3ced86d2f455275efa20cf)
- `senaite.core` (v1.3.0) [@d34ace1](https://github.com/senaite/senaite.core/tree/d34ace15baa63252da530a5ed256bcaead8eb4c8)
- `senaite.core.listing` [@e32a7f6](https://github.com/senaite/senaite.core.listing/tree/e32a7f60e605604f3408bd5cdc7b35cde696648f)
- `senaite.core.supermodel`[@e8fdad1](https://github.com/senaite/senaite.core.supermodel/tree/e8fdad119025c9be2299a76e51946a7007f92177)
- `senaite.impress`[@bcd1409](https://github.com/senaite/senaite.impress/tree/bcd14095901c5118a7133480ea5b7914c43873df)
- `senaite.jsonapi` [@871959f](https://github.com/senaite/senaite.jsonapi/tree/871959f4b1c9edbb477e9456325527ca78e13ec6)
- `senaite.lims` [@8423456](https://github.com/senaite/senaite.lims/tree/8423456f46023c6859d71c71c00db9c931754a4d)

### Deployment notes

Estimated time for update/deployment completion: 2.5h - 3h

- Upgrade `senaite.core` version 1.3
- Reinstall (QuickInstaller) `senaite.lims` 
- Reinstall (QuickInstaller) `senaite.impress` 
- Reinstall (QuickInstaller) `bhp.lims`

### Differences with production

#### BHP.LIMS Add-on

- #212 Grading of results functionality
- #211 Invalidation of results after verification gives an error
- #204 Email of results should have a PID
- #202 Unable to activate bhp.lims add-on using an empty database
- #201 Viral Load quantifier drop down menu does not have an = sign
- #200 Retracted results are listed in results report
- #198 Display Remarks in results reoprts
- #197 Allow the labman to manually set the Assay Date
- #195 Visit Code should be included on delivery checklist
- #193 Allow editing of analysis request once created
- #191 Filter analysis request by test requested
- #190 Analysis Request table should include visit number
- #188 Verifier is not displayed in some results reports
- #185 Results for haematology does not get published
- #184 Results email comes with no attachment
- #183 Delivery checklist should have date received
- #182 Result report has no Assay Date. Date Tested
- #181 Percentage of progress does not show when doing reception and sending to point of testing
- #180 Results for haematology does not get published
- #179 Add column for PID
- #178 Emails do not have an attachment results from after publishing results
- #159 The system should allow clients to print requisition forms from AR page
- #130 Cannot configure the body from the email message sent when a sample is invalidated

### Relevant changes in other add-ons

- [SC#1286](https://github.com/senaite/senaite.core/pull/1286) Detection Limit selector is not saved on submit
- [SC#1287](https://github.com/senaite/senaite.core/pull/1287) Minor performance improvements in analyses
- [SC#1284](https://github.com/senaite/senaite.core/pull/1284) Secondary Sample functionality
- [SC#1289](https://github.com/senaite/senaite.core/pull/1289) Adding Analyses to an existing Worksheet in a non-open status
- [SC#1290](https://github.com/senaite/senaite.core/pull/1290) Retracting a calculated analysis leads to an inconsistent state
- [SC#1291](https://github.com/senaite/senaite.core/pull/1291) Allow the removal of empty worksheets
- [SC#1293](https://github.com/senaite/senaite.core/pull/1293) Linking Lab Contacts to LDAP-user not possible
- [SC#1268](https://github.com/senaite/senaite.core/pull/1268) Adding Facscalibur import instrument interface
- [SC#1271](https://github.com/senaite/senaite.core/pull/1271) Fixing cobas integra instrument import interface
- `senaite.core`: [(v1.2.9.1 - v1.3.0) Diff 1.2.9 - 1c1ab4b](https://github.com/senaite/senaite.core/compare/1.2.9...d34ace1)

*SC: changes in `senaite.core` add-on*
*For the full list of changes from v1.2.9.1 to v.1.3 check [senaite.core's changelog](https://github.com/senaite/senaite.core/blob/master/CHANGES.rst#changelog)*


## 190314 (19-03-14)

### Versions

- `bhp.lims` [@e65413f](https://github.com/bhp-lims/bhp.lims/tree/e65413f0b2601d8b606a434070d8ca57cd54c969)
- `senaite.api` [@c79c53a](https://github.com/senaite/senaite.api/tree/c79c53abcbe6e3a5ab3ced86d2f455275efa20cf)
- `senaite.core` (v1.3.0) [@1c1ab4b](https://github.com/senaite/senaite.core/tree/1c1ab4b0d2c8c09f89384c8e412e406fba698ac0)
- `senaite.core.listing` [@e1783c1](https://github.com/senaite/senaite.core.listing/tree/e1783c1dbce23efe4ce26a99e9ffbff372c6aaf0)
- `senaite.core.supermodel`[@e8fdad1](https://github.com/senaite/senaite.core.supermodel/tree/e8fdad119025c9be2299a76e51946a7007f92177)
- `senaite.impress`[@bcd1409](https://github.com/senaite/senaite.impress/tree/bcd14095901c5118a7133480ea5b7914c43873df)
- `senaite.jsonapi` [@871959f](https://github.com/senaite/senaite.jsonapi/tree/871959f4b1c9edbb477e9456325527ca78e13ec6)
- `senaite.lims` [@8423456](https://github.com/senaite/senaite.lims/tree/8423456f46023c6859d71c71c00db9c931754a4d)

### Deployment notes

Estimated time for update/deployment completion: 2.5h - 3h

- Upgrade `senaite.core` version 1.3
- Reinstall (QuickInstaller) `senaite.lims` 
- Reinstall (QuickInstaller) `senaite.impress` 
- Reinstall (QuickInstaller) `bhp.lims`

### Differences with production

#### BHP.LIMS Add-on

- #204 Email of results should have a PID
- #202 Unable to activate bhp.lims add-on using an empty database
- #201 Viral Load quantifier drop down menu does not have an = sign
- #200 Retracted results are listed in results report
- #198 Display Remarks in results reoprts
- #197 Allow the labman to manually set the Assay Date
- #195 Visit Code should be included on delivery checklist
- #193 Allow editing of analysis request once created
- #191 Filter analysis request by test requested
- #190 Analysis Request table should include visit number
- #188 Verifier is not displayed in some results reports
- #185 Results for haematology does not get published
- #184 Results email comes with no attachment
- #183 Delivery checklist should have date received
- #182 Result report has no Assay Date. Date Tested
- #181 Percentage of progress does not show when doing reception and sending to point of testing
- #180 Results for haematology does not get published
- #179 Add column for PID
- #178 Emails do not have an attachment results from after publishing results

### Relevant changes in other add-ons

- `senaite.core`: [Diff 1.2.9 - 1c1ab4b](https://github.com/senaite/senaite.core/compare/1.2.9...1c1ab4b#diff-db23dcd814354c954091a9b90dbfd92a)


## 190130 (19-01-30)

- `bhp.lims` [@068fa16](https://github.com/bhp-lims/bhp.lims/tree/068fa1677de3d4da89a4595cf93f69db53d13c83)
- `senaite.api` [@c79c53a](https://github.com/senaite/senaite.api/tree/c79c53abcbe6e3a5ab3ced86d2f455275efa20cf)
- `senaite.core` (v1.2.9.2) [@e460cf6](https://github.com/senaite/senaite.core/tree/e460cf662d7a64c37d086e9cc03a0abe8905143e)
- `senaite.core.supermodel`(v1.1.0) [@bbcffac](https://github.com/senaite/senaite.core.supermodel/tree/bbcffac883526daf79c8ffb8d4299116094f4e14)
- `senaite.impress` (v1.1.0) [@f070925](https://github.com/senaite/senaite.impress/tree/f0709257b6536074b8cfe05212a47565c46fb8c2)
- `senaite.jsonapi` [@871959f](https://github.com/senaite/senaite.jsonapi/tree/871959f4b1c9edbb477e9456325527ca78e13ec6)
- `senaite.lims` [@3137ae4](https://github.com/senaite/senaite.lims/tree/3137ae4b4940c50a72b30291ad45dc85b3c179ee)
