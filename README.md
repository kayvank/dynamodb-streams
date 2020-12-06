dynamodb-streams
---

dynamodb-streams is a python3 serverless project that persistes  dynamodb changes of interest to AWS s3


## Intallation
* Dependencies
* Install Source
* Tests
* Enironment valiables

### Dependencies

- [serverless framework](https://www.serverless.com/)
- [python virtualenv](https://python-guide-pt-br.readthedocs.io/pt_BR/latest/dev/virtualenvs.html)
- [npm](https://www.npmjs.com/get-npm)

### Install Source 

``` sh
npm install -g serverless
cd dynamodb-stream.git
virtualenv venv --python=python3
source venv/bin/activate
```

### Tests

![unit-test](./docs/img/unit-test.jpg)

``` sh
pip install pytest-watch 
ptw
```

### Enironment variables

``` sh
export PYTHONPATH="~/dynamodb-streams-lambda/src"
export AWS_REGION='us-east-1'
export AWS_ACCEWSS_KEY_ID= 'my-aws-access-key'
export AWS_SECRET_ACCESS_KEY='my-secret-key'
```

### Local deployment
make sure your environmnet variables are set

``` sh
serverless deploy -s local -v
```

## References
- [serverless framework](https://www.serverless.com/)
- [aws fireohose](https://aws.amazon.com/kinesis/data-firehose/)
- [dynamodb streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)
