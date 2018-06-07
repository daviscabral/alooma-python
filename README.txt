# Alooma's Python SDK
Manage your real-time data pipeline with Alooma's Python SDK. Our Python SDK allows you to perform all the operations enabled by our UI and more with Python code.

## Getting started

```python
import alooma

alooma = alooma.Alooma(hostname="<your sub-domain>.alooma.io", username="<your username>", password="<your password>")
```

### get_config()
To get the system's configuration, use:
```python
config = alooma.get_config()
```

## get_structure()
To get your system's structure, use:
```python
structure = alooma.get_structure()
```

## get_mapping_mode()
To get your system's mapping mode (FLEXIBLE/STRICT), use:
```python
mapping_mode = alooma.get_mapping_mode()
```
## Not yet documented functions:

* `create_s3_input(name, key, secret, bucket, prefix, load_files, transform_id)`
* `create_mixpanel_input(mixpanel_api_key, mixpanel_api_secret, from_date, name, transform_id)`
* `create_input(input_post_data)`
* `get_transform_node_id`
* `remove_input(input_id)`
* `set_transform_to_default()`
* `set_mapping(mapping, event_type_name)`
* `set_mapping_mode(flexible)`
* `discard_event_type(event_type_name)`
* `discard_field(mapping, field_path)`
* `unmap_field(mapping, field_path)`
* `map_field(schema, field_path, column_name, field_type, non_null, **type_attributes)`
* `find_field_name(schema, field_path, add_if_missing=False)`
* `get_input_sleep_time(id)`
* `set_input_sleep_time(id, sleep_time)`
* `get_samples_status_codes()`
* `get_samples_stats()`
* `get_samples(event_type=None, status_codes=None)`
* `get_all_transforms()`
* `get_transform(module_name='main')`
* `set_transform(transform, module_name='main')`
* `test_transform(sample, temp_transform=None)`
* `test_transform_all_samples(event_type, status_code)`
* `get_incoming_queue_metric(minutes)`
* `get_throughput_by_name(name)`
* `get_incoming_events_count(minutes)`
* `get_average_event_size(minutes)`
* `get_max_latency(minutes)`
* `get_tables()`
* `get_notifications(epoch_time)`
* `get_plumbing()`
* `get_redshift_config()`
* `clean_system()`
* `remove_all_inputs()`
* `delete_all_event_types()`
* `delete_event_type(event_type)`
* `get_event_types()`
* `get_event_type(event_type_name)`
* `set_settings_email_notifications(email_settings_json)`
* `delete_s3_retention()`
* `clean_restream_queue()`
* `start_restream()`
* `get_restream_queue_size()`
