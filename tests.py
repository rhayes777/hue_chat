from chat_bot import trim


def test_remove_characters():
    string = """Here is the list of JSONs:

```
[
  {
    "light_id": 0,
    "color": {
      "hue": 7281,
      "saturation": 254,
      "brightness": 254
    }
  },
  { 
    "light_id": 1,
    "color": {
      "hue": 7281,
      "saturation": 254,
      "brightness": 254
    }
  }
]
```"""
    assert trim(string) == """[
  {
    "light_id": 0,
    "color": {
      "hue": 7281,
      "saturation": 254,
      "brightness": 254
    }
  },
  { 
    "light_id": 1,
    "color": {
      "hue": 7281,
      "saturation": 254,
      "brightness": 254
    }
  }
]"""