import boto3
from abc import ABC, abstractmethod
from config.constants import S3_SERVICE, AWS_REGION


class StorageResourceInterface(ABC):
    @classmethod
    @abstractmethod
    def load(cls):
        pass

    def upload(self, path):
        pass


class DefaultStorageResource(StorageResourceInterface):
    service = S3_SERVICE
    region = AWS_REGION
    bucket = "ebanx-transactions"
    default_key = "transactions.json"

    def __init__(self, service, region):
        self.service = service
        self.region = region
        self.client = boto3.client(self.service, self.region)

    @classmethod
    def load(cls):
        return cls(cls.service, cls.region)

    def upload(self, path):
        return self.client.upload_file(path, Bucket=self.bucket, Key=self.default_key)

    def upload_obj(self, obj, key):
        return self.client.put_object(
            Body=obj,
            Bucket=self.bucket,
            Key=key,
            ContentType='application/json'
        )

    def _set_bucket(self, bucket):
        self.bucket = bucket
        return self

    def _set_key(self, key):
        self.default_key = key
        return self
