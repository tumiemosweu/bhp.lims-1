# Releases

## 190314 (19-03-14)

### Versions

- `bhp.lims` [@e65413f](https://github.com/bhp-lims/bhp.lims/tree/e65413f0b2601d8b606a434070d8ca57cd54c969)
- `senaite.api` [@c79c53a](https://github.com/senaite/senaite.api/tree/c79c53abcbe6e3a5ab3ced86d2f455275efa20cf)
- `senaite.core` [@1c1ab4b](https://github.com/senaite/senaite.core/tree/1c1ab4b0d2c8c09f89384c8e412e406fba698ac0)
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
