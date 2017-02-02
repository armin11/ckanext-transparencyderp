ckanext-transparencyderp
========================

This extension should provide functionality to use ckan as a 
central transparency portal. In this case, ckan is used to serve
different datatypes which has own models which are managed by
ckanext-scheming. The extension adopt the facet list and the search
form to show the translated titles from the different schemes which
are defined as ckanext-scheming json files. One adoption, is possibility
to have a dataset_type_label object for different languages. This allows 
an internationalized dropdown menu for choosing a different form for 
each dataset_type. The translation of json based classifications is done 
by the use of one central schema with "dataset_type": "dataset". This 
schema is hidden in the dropdown list and includes all classifications
(for packages and resources).

Requirements
============

This plugin is developed under usage of CKAN 2.5.3 Ubuntu 14.04 package.
It requires ckanext-scheming.

Configuration
=============

Set the schemas you want to use with configuration options (ckans .ini file) and activate the search for all packages by default:

```ini
## Search all packages not only dataset
ckan.search.show_all_types = true

ckan.plugins = scheming_datasets

#   module-path:file to schemas being used
scheming.dataset_schemas = ckanext.transparencyderp:ckan_dataset_rp.json
                           ckanext.transparencyderp:ckan_govdata_1.json                                    			    				   ckanext.transparencyderp:ckan_decision_rp_1.json
                           ckanext.transparencyderp:ckan_govdata_full_1_1.json

# scheming.dataset_schemas = http://example.com/spatialx_schema.json

#   Preset files may be included as well. The default preset setting is:
scheming.presets = ckanext.scheming:presets.json

#   The is_fallback setting may be changed as well. Defaults to false:
scheming.dataset_fallback = false
```

Adoption of solr configuration
==============================

```xml
    <!-- field for custom resource choice lists-->
    <field name="res_extras_res_transparency_document_change_classification" type="string" indexed="true" stored="true" multiValued="false"/>

    <dynamicField name="extras_*" type="text" indexed="true" stored="true" multiValued="false"/>
    <dynamicField name="res_extras_*" type="text" indexed="true" stored="true" multiValued="true"/>
    <dynamicField name="vocab_*" type="string" indexed="true" stored="true" multiValued="true"/>
    <dynamicField name="*" type="string" indexed="true"  stored="false"/>
    <field name="transparency_category_de_rp" type="string" indexed="true" stored="true" multiValued="false"/>
    <field name="govdata_categories" type="string" indexed="true" stored="true" multiValued="true"/>
```
