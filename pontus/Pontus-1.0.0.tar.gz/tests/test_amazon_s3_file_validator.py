# -*- coding: utf-8 -*-
import pytest
import botocore
import boto3
from flexmock import flexmock

from pontus import AmazonS3FileValidator
from pontus.exceptions import FileNotFoundError, ValidationError
from pontus.validators import BaseValidator

HOUR_IN_SECONDS = 60 * 60


class CustomValidator(BaseValidator):
    def __call__(self, obj):
        if obj.key != 'test-unvalidated-uploads/images/hello.jpg':
            raise ValidationError('Invalid.')


class TestAmazonS3FileValidator(object):
    @pytest.fixture
    def amazon_s3_file_validator(self, bucket):
        key_name = 'test-unvalidated-uploads/images/hello.jpg'
        boto3.resource('s3').Object(bucket.name, key_name).put(Body='test')
        return AmazonS3FileValidator(
            key_name=key_name,
            bucket=bucket,
            validators=[CustomValidator()]
        )

    @pytest.fixture
    def failing_amazon_s3_file_validator(self, bucket):
        key_name = 'images/fail.jpg'
        boto3.resource('s3').Object(bucket.name, key_name).put(Body='test')
        return AmazonS3FileValidator(
            key_name=key_name,
            bucket=bucket,
            validators=[CustomValidator()]
        )

    def test_validate_calls_validators(self, amazon_s3_file_validator):
        (
            flexmock(CustomValidator)
            .should_receive('__call__')
            .with_args(amazon_s3_file_validator.obj)
            .and_return(True)
        )
        amazon_s3_file_validator.validate()

    def test_validate_returns_true_when_validation_passes(
        self,
        amazon_s3_file_validator
    ):
        assert amazon_s3_file_validator.validate()

    def test_validator_has_no_errors_when_validation_passes(
        self,
        amazon_s3_file_validator
    ):
        assert not amazon_s3_file_validator.errors

    def test_validate_returns_false_when_validation_fails(
        self,
        failing_amazon_s3_file_validator
    ):
        assert not failing_amazon_s3_file_validator.validate()

    def test_validator_has_errors_when_validation_fails(
        self,
        failing_amazon_s3_file_validator
    ):
        failing_amazon_s3_file_validator.validate()
        assert failing_amazon_s3_file_validator.errors == ['Invalid.']

    def test_throws_error_if_file_not_found(
        self,
        bucket
    ):
        with pytest.raises(FileNotFoundError):
            AmazonS3FileValidator(
                key_name='does_not_exist.jpg',
                bucket=bucket
            )

    def test_validate_removes_unvalidated_prefix_if_validation_passes(
        self,
        amazon_s3_file_validator,
        bucket
    ):
        amazon_s3_file_validator.validate()

        with pytest.raises(botocore.exceptions.ClientError):
            boto3.resource('s3').Object(
              bucket.name, 'test-unvalidated-uploads/images/hello.jpg'
            ).get()

        assert boto3.resource('s3').Object(
              bucket.name, 'images/hello.jpg'
        ).get()
        assert not amazon_s3_file_validator.obj.key.startswith(
            'test-unvalidated-uploads/'
        )

    def test_repr(self, amazon_s3_file_validator):
        assert repr(amazon_s3_file_validator) == (
            "<AmazonS3FileValidator " +
            "key='test-unvalidated-uploads/images/hello.jpg'>"
        )
