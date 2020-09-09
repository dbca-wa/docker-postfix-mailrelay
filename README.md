# docker-postfix-postmaps
Based on boky/postfix, with simple support for sender_canonical and sender_bcc maps

## Usage
In addition to the boky/postfix image options, postmaps.sh will automatically create postmap files in /etc/postmaps on launch. This allows for injection of postmap hash files using kubernetes config like below:

```yaml
apiVersion: v1
data:
  sender_bcc_maps: |-
    # sender_address bcc_address
    robotman@doom.patrol cliff.steele@doom.manor
  sender_canonical_maps: |-
    # sender_address destination_rewrite
    # no change for trusted senders
    /^(cyborg@doom.patrol)$/ ${1}
    # no change for addresses containing noreply@
    /^(.*noreply@.*)$/ ${1}
    # expand empty addresses and missing domains
    /^$/ noreply@doom.patrol
    /^([^@]+)$/ ${1}+noreply@doom.patrol
    # rewrite addresses without noreply to include it
    /^(.+)@(.+)$/ ${1}+noreply@${2}
kind: ConfigMap
```
Then mount the vol and can use env vars to configure various maps
```yaml
TODO
```
