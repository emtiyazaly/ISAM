# IBM ISAM RAPI operations with Python

The repository consist of simple python scripts for performaing different operations using the ISAM Rest-APIs on bulk Appliances in different environments.
i.e. creating a user for providing read only access to a colloborating team requires creating the user on lots of ISVA Appliances.
The scritps also provide logs in a /log directory & logs to console with all detials of the operation.

Note: The scripts are in any way provided by officially by IBM & you will be running at your own risk.

## Usage/Examples

```python
# Open scripts in a text editor and change the following
# - User details [username, password, group-ids & username/newPassword in-case of changePassword]
# - Server Details [include FQDN/IP, LMI username & password of user with operation execution privilages

python -u "<path>/createUserISAM.py"
python -u "<path>/changePasswordISAM.py"
```

## Scritps

- createUserISAM.py - creates a ISAM LMI user & deploys changes.
- changePasswordISAM.py - Changes password of an existing LMI user

## Authors

- [@emtiyazaly](https://www.github.com/emtiyazaly)

## Documentation

[IBM ISAM RAPI documentation](https://www.ibm.com/docs/en/sva/10.0.7?topic=developing-rest-api-documentation)
