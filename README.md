## What is Alooma.py?

Alooma.py is a powerful and convenient way to set up and manage your Alooma platform programmatically. Alooma.py is set up to easily chain commands for common use cases, and there are even some features exposed through alooma.py which are not exposed through Alooma's UI.

Alooma.py lets you programmatically perform all the basics of operating the Alooma platform:

- [Create and manage your inputs and mappings](#creating)
- [Write, test, and deploy the code that runs on your stream](#using)
- [Troubleshoot your event streams](#trouble)
- [Query system metrics](#querying)

## Getting started

- To install alooma.py simply run:  

  ```shell
  sudo pip install alooma
  ```

- Connect to your Alooma system by creating an instance:

  ```python
  import alooma
  api = alooma.Client(username="<YOUR_USERNAME>", password="<YOUR_PASSWORD>")

  # If you have an API key, you may use it instead of your username and password
  # by specifying it in the constructor:
  api = alooma.Client(api_key="<YOUR_API_KEY>")

  # If you have more than one Alooma instance, you can choose the instance you want to
  # log into by specifying it in the constructor:
  api = alooma.Client(username="<YOUR_USERNAME>", password="<YOUR_PASSWORD>",
                      account_name="<YOUR_ACCOUNT_NAME>")
  ```

  ​

## Creating and mapping an input

To set up your inputs programmatically instead of via UI, you can follow this example sequence.

- Call `input_data = api.get_inputs(...)` to get an existing input of the same type you want to create. `get_inputs` can find inputs by a given name, type, or ID. See the docstring for `get_inputs` for more details.

- Copy the configuration from`input_data`, edit the fields you need, and create a new input:

  ```python
  new_input_config = dict(input_data['configuration'])
  new_input_config['...']] = '...'
  api.create_input({
  	'name': '<name for the new input>',                  
  	'type': input_data['type'],
  	'configuration': new_input_config
  })
  ```

  - Note that this flow does not support any inputs that require OAuth (such as Google Adwords or Google Analytics), Custom Webhooks, or any of the SDKs.
  - Set `one_click` to False if you want to manage table creation and mapping for this input.
  - On success the function returns a string representing the created input ID.  
    On failure, an exception is raised.

- Call `api.get_event_types()` to get a list of event types that exist in the system and their mapping status. Each element in the returned list is a dictionary containing these keys:

  - `name`: the name of the event type.
  - `mappingMode`: `['AUTO_MAP'|'FLEXIBLE'|'STRICT']`, a string representing the mapping mode of this event type.
  - `origInputLabel`: the name of the input that created this event type.
  - `mapping`: a dict containing information about the mapping for this event type. Contains `isDiscarded` (boolean), `tableName` (string), and `schema` (string).
  - `consolidation`: a dict containing information about consolidations for this event type.

- Call `api.get_event_type(event_type_name)` to get the mapping set for any specific event, along with all its fields and sample values for each field. `api.get_mapping(event_type_name)` is similar, except it returns only information about the mapping, without sample values.

- Set the mapping for an event type by calling `api.set_mapping(mapping, event_type_name)` and passing it a mapping object. You can modify the one you got from `get_mapping`.

  - On success the function returns an HttpResponse object with status code 2XX.  
    On failure, an exception is raised.

- Note that you can get a list of available tables in the target output using `api.get_tables()`. If the table you want to map to doesn't exist, you'll have to create it in the target output, manually, or by using `api.create_table(...)`.

## Using the Code Engine

A scenario where alooma.py provides capability not exposed in the UI is the ability to break up your code into modules in the Code Engine. Code sub-modules can be used to encapsulate logic, just as a Python module would be used. It can also be used as a means to store configuration, allowing the user to easily update this configuration via code. Note that sub-modules should not exceed 10,000 lines of code.

- You can start by getting the current code from the Code Engine with `api.get_transform(module_name='main')`. Pass a module name if you want a specific module, otherwise it will return the main code block (which is also the code you view in the UI).

- You can get all the modules defined in the system using `api.get_all_transforms()`. This returns a dictionary which reflects modules names and their content.

- Deploy code to the Code Engine using `api.set_transform(code, module_name='main')`

  - If a module name is not passed, it will set the "main" module.
  - On success the function returns an HttpResponse object with status code 2XX.  
    On failure, an exception is raised.
  - Note that you can delete a module by setting it with an empty code block.

- Example:

  ```python
  import alooma
  # connect to Alooma API
  api = alooma.Alooma(
      'app.alooma.com',
      '<YOUR USERNAME>',
      '<YOUR PASSWORD>',
      port=443)

  # submit a code module, and name it 'submodule'.
  # this module contains a dict called 'transform_names'
  # and a method called 'transform_ft_to_mtr'

  api.set_transform("""
  transform_names = {'John': 'Jonathan',
                     'Bob': 'Robert',
                     'Rick': 'Richard'}

  def transform_ft_to_mtr(x):
      return x * 0.3048

  """, module_name='submodule')

  # Now edit the main code to use 'submodule' by importing it.
  # This step can equivalently be done via the Alooma UI
  # by editing the code in the Code Engine.
  # Note that it should only be run once - if you later re-submit the
  # 'configs' module, it will be automatically re-loaded by
  # the main module, so the code that runs in the production

  api.set_transform("""
    import submodule

    def transform(event): 
      event['name'] = submodule.transform_names.get(event['name'], event['name'])  
      # The above line is equivalent to: # if event['name'] in submodule.transform_names: 
      #     event['name'] = submodule.transform_names[event['name']] 

      if 'value' in event:
        event['value'] = submodule.transform_ft_to_mtr(event['value'])
      return event

     """, module_name=main')
  ```

As any good developer knows, you don't just go and deploy code without testing it! [Learn more about how to test your Code Engine code](https://support.alooma.com/hc/en-us/articles/115000067989-Testing-your-code-programatically) using alooma.py.

## Troubleshooting problematic events

In the case where you have errors in Alooma, you may want to pull the notification information and address the events that created errors.

- Call `api.get_notifications(epoch_time)` to pull a list of notifications between some time (seconds since epoch) and now.  
  This returns a dictionary with `messages as a key and a list of the notifications in ascending time order as its value.`
- Address the errors reported in the notifications by either changing the mapping or the Code Engine code with `api.set_mapping(mapping, event_type)` or `api.set_transform(code, module_name='main')`, described above.
- Start the restream to re-run all the events that were in the Restream Queue with `api.start_restream()`.
- If for any reason you need to stop the restream mid-stream, you can run stop it with `api.stop_restream()`.
- Pull the list of notifications again to address the next issue.

## Querying system metrics

Alooma exposes a set of metrics which you can use to track the health and status of your data-pipeline.

- Call `get_metrics_by_names(metric_names, minutes)` to get system metrics. 

- `metric_names` is either one or a list of supported metric names, and `minutes` is minutes back from the current time.

- The various metric names are:

  ```
  'EVENTS_IN_PIPELINE',
  'UNMAPPED_EVENTS',
  'IGNORED_EVENTS',
  'ERROR_EVENTS',
  'LOADED_EVENTS_RATE'
  ```

- The return value is a list, with the same size and order as:`metric_names`, where each element is a dictionary with `datapoints` and `target` keys. `target` is the name of the metric, and `datapoints` is an array of 2-tuples of `(value, timestamp)`.

Those are the basics - you're ready to use alooma.py! Feel free to [contact us](mailto:support@alooma.com) if you have any questions. 
