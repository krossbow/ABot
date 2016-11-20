# Customizing

This is a guide on customizing ABot to suit your preferences, do note that most of this requires minimal Python programming knowledge (as of version 1.0)

## Name:

The bot's name can be changed by changing the `__name__` object in the main.py file, it defaults to "ABot".

```
__name__ = "ABot" # Program name.
```

## Prefix:

The bot's prefix for commands is *auto-set* to the first letter of `__name__` with a '!' appended to it.
It is used for parsing commands - example:

`A!help`

