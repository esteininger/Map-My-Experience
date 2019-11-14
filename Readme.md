# Map My Experience

Map My Experience is a simple app that superimposes all the photos you took during a trip onto a clickable route.

![Mockup](https://raw.githubusercontent.com/esteininger/Map-My-Experience/master/static/misc/ezgif-4-51254a8dd7f9.gif)


[View Live Version](https://phoroll.com)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies.

```bash
pip install -r requirements.txt
```

## Usage

Modify run.py variables:

```python
file_folder = os.path.dirname(os.path.abspath(__file__)) + '/static/img/map-my-experience'
file_ext = '.JPG'
```

Modify map.html API KEY to include Google Maps API:

```html
    <script async defer src="https://maps.googleapis.com/maps/api/js?key=API_KEY_HERE&callback=initMap">
    </script>
```

Modify map.html javascript variable:

```javascript
{"image": `/abs/path/of/images/${item.image_path}`}
```

To run:

Drag all your photos taken during your trip to ```/static/images/``` and run:

```shell
python run.py
```

Navigate to http://localhost:5011 to view


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
