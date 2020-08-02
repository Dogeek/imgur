# Imgur - A python wrapper around imgur's API
^^because imgurpython has been deprecated

## Installation

### Using pip

`pip install imgur`

### From source

```bash
git clone https://github.com/dogeek/imgur.git
cd imgur
python3 setup.py install
```

## Documentation

Documentation will be hosted on readthedocs.io [TBD]

## Example

```python
from imgur import Imgur

client = Imgur(client_id, client_secret, access_token, refresh_token)
image = client.image.upload('https://picsum.photos/200/300', name='A great picture!', description='My summer vacation')
image.favorite()
image.delete()
```

## TODO

- [ ] Implement the Gallery model and its controller
- [ ] Implement exceptions
- [ ] Implement the Account model(s) and its controller(s)
- [ ] write documentation
- [ ] add models.image.Image.add_to_album() convenience method.
