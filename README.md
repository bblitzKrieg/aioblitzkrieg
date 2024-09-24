## **[@BlitzkriegAutobot](https://t.me/BlitzkriegAutobot) asynchronous api wrapper**
**Docs:** https://blitzkrieg-api.readme.io


**Install**
``` bash
pip install aioblitzkrieg
```

**Basic methods**
``` python
from aioblitzkrieg import AioBlitzkrieg

client = AioBlitzkrieg(api_key='863...e12')

me = await client.get_me()
archives = await client.get_archives()
report = await client.report_archive(archive_id_id=1)

print(me, archives, report, sep='\n')
```

**Upload archive method**
``` python
from aioblitzkrieg import AioBlitzkrieg

client = AioBlitzkrieg(api_key='863...e12')

path = "sample.zip"

result = await client.upload_archive(
    file_path=path
)
print(result)

# Upload archive via unique identifier of the referral partner

ref_id = 'MY_SERVICE_REF_ID'

result = await client.upload_archive(
    file_path=path,
    ref_id=ref_id
)
print(result)
```