from troposphere import (
    Output,
    GetAtt,
)

from troposphere.s3 import (
    Bucket,
    PublicRead,
    VersioningConfiguration,
)

from troposphere.cloudfront import (
    DefaultCacheBehavior,
    Distribution,
    DistributionConfig,
    ForwardedValues,
    Origin,
    S3Origin,
)

from .template import template


# Create an S3 bucket that holds statics and media
assets_bucket = template.add_resource(
    Bucket(
        "AssetsBucket",
        AccessControl=PublicRead,
        VersioningConfiguration=VersioningConfiguration(
            Status="Enabled"
        ),
        DeletionPolicy="Retain",
    )
)


# Output S3 asset bucket name
template.add_output(Output(
    "AssetsBucketDomainName",
    Description="Assets bucket domain name",
    Value=GetAtt(assets_bucket, "DomainName")
))


# Create a CloudFront CDN distribution
distribution = template.add_resource(
    Distribution(
        'AssetsDistribution',
        DistributionConfig=DistributionConfig(
            Origins=[Origin(
                Id="Assets",
                DomainName=GetAtt(assets_bucket, "DomainName"),
                S3OriginConfig=S3Origin(
                    OriginAccessIdentity="",
                ),
            )],
            DefaultCacheBehavior=DefaultCacheBehavior(
                TargetOriginId="Assets",
                ForwardedValues=ForwardedValues(
                    QueryString=False
                ),
                ViewerProtocolPolicy="allow-all",
            ),
            Enabled=True
        ),
    )
)


# Output CloudFront url
template.add_output(Output(
    "AssetsDistributionDomainName",
    Description="The assest CDN domain name",
    Value=GetAtt(distribution, "DomainName")
))
