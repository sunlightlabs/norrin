# Norrin

Conveying messages with the force of the Power Cosmic.

Norrin provides services used by [Congress for iOS](https://github.com/sunlightlabs/congress-ios).

## Remote Configuration

*appconfig* is used to publish remote configuration that is loaded by the iOS application using [GroundControl](https://github.com/mattt/GroundControl). A default configuration is loaded on app launch, allowing an opportunity to override or update settings. A URL scheme can be used to have the iOS app read and update configuration from an arbitrary *appconfig* configuration.

## Notifications

*notifications* is used to create, queue, and send push notifications. Data is loaded from the [Sunlight Congress API](https://sunlightlabs.github.io/congress/) and notifications are created based on the categories defined in Congress for iOS. Once queued, a configurable set of adapters handle the notifications. These adapaters can write the notifications to a log file, send via email, or send using [Urban Airship](http://urbanairship.com).

Notifications that are pending or failed can be reprocessed by the adapter pipeline.

## Settings

All of the following settings should be set using environment variables.

### Urban Airship

| Variable                   | Default Value |
|----------------------------|---------------|
| UA_KEY                     | None |
| UA_SECRET                  | None |
| UA_MASTER                  | None |

### MongoDB

| Variable                   | Default Value |
|----------------------------|---------------|
| MONGODB_HOST               | localhost |
| MONGODB_PORT               | 27017 |
| MONGODB_DATABASE           | norrin |
| MONGODB_USERNAME           | None |
| MONTODB_PASSWORD           | None |

### Sentry

| Variable                   | Default Value |
|----------------------------|---------------|
| SENTRY_DSN                 | None |

### Celery

| Variable                   | Default Value |
|----------------------------|---------------|
| CELERY_BROKER              | None |

### Sunlight API

| Variable                   | Default Value |
|----------------------------|---------------|
| SUNLIGHT_API_KEY           | None |

### Django

| Variable                   | Default Value |
|----------------------------|---------------|
| DATABASE_URL               | None |
| SECRET_KEY                 | None |
