Start localstack
```
localstack start
```

create s3 bucket
```
awslocal s3api create-bucket --bucket test-bucket
```

list s3 buckets
```
awslocal s3api list-buckets
```

delete s3 bucket
```
awslocal s3api list-objects --bucket test-bucket

awslocal s3api delete-objects --bucket test-bucket --delete "$(awslocal s3api list-objects --bucket <bucket-name> --query '{Objects: Contents[].{Key: Key}}' --output json)"

awslocal s3api delete-bucket --bucket test-bucket

```


create sqs
```
awslocal sqs create-queue --queue-name test-queue
```

list sqs
```
awslocal sqs list-queues
```

delete sqs
```
awslocal sqs delete-queue --queue-url http://localhost:4566/000000000000/test-queue

```


zip lambda with node_modules
```
zip -r function.zip index.js node_modules
```

create your function based on zip
```
awslocal lambda create-function \
    --function-name localstack-lambda-url-example \
    --runtime nodejs18.x \
    --zip-file fileb://function.zip \
    --handler index.handler \
    --role arn:aws:iam::000000000000:role/lambda-role
```

*--- after your function is created check the status of the lambda with list step ---*

delete you function 
```
awslocal lambda delete-function --function-name localstack-lambda-url-example
```


show list of functions
```
awslocal lambda list-functions
```

execute your lambda
```
curl -X POST \
  http://localhost:4566/2015-03-31/functions/localstack-lambda-url-example/invocations \
  -d '{"body": "{\"num1\": \"10\", \"num2\": \"10\"}"}' \
  -H "Content-Type: application/json"
```


my custom for easy check on local env
```
awslocal lambda delete-function --function-name localstack-lambda-url-example

zip -r function.zip index.js node_modules


awslocal lambda create-function \
    --function-name localstack-lambda-url-example \
    --runtime nodejs18.x \
    --zip-file fileb://function.zip \
    --handler index.handler \
    --role arn:aws:iam::000000000000:role/lambda-role


curl -X POST \
  http://localhost:4566/2015-03-31/functions/localstack-lambda-url-example/invocations \
  -d '{"body": "{\"num1\": \"10\", \"num2\": \"10\"}"}' \
  -H "Content-Type: application/json"
```
