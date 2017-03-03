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
To enable spatial search and spatial attributed metadata also ckanext-spatial
is needed. The german translation of ckanext-spatial(s) search window title and clear
button is included in the .po file.

Requirements
============

This plugin is developed under usage of CKAN 2.5.4 Ubuntu 14.04 package.
It requires ckanext-scheming and optional ckanext-spatial.

Installation
============

```{r, engine='bash', create_postgis_extension_for_ckanext-spatial}
    sudo apt-get install python-dev libxml2-dev libxslt1-dev libgeos-c1
    su postgres
    createuser  -S -D -R -P ckan_2.5.2
    createdb  -O ckan_2.5.2 ckan_2.5.2 -E utf-8
    psql -d ckan_2.5.2 -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql
    psql -d ckan_2.5.2 -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql
    psql -d ckan_2.5.2 -c 'ALTER TABLE geometry_columns OWNER TO "ckan_2.5.2"'
    psql -d ckan_2.5.2 -c 'ALTER TABLE spatial_ref_sys OWNER TO "ckan_2.5.2"'
    exit
```

```{r, engine='bash', install_ckanext-spatial}
    ./usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/
    pip install -e "git+https://github.com/okfn/ckanext-spatial.git#egg=ckanext-spatial"
    cd /usr/lib/ckan/default/src/ckanext-spatial/
    pip install -r pip-requirements.txt
    #maybe remove pyparsing because newer version is already installed in ubuntu package version
    #python setup.py develop
    deactivate
```

```{r, engine='bash', install_ckanext-scheming}
    ./usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/
    pip install -e 'git+https://github.com/ckan/ckanext-scheming.git#egg=ckanext-scheming'
    cd /usr/lib/ckan/default/src/ckanext-spatial/
    pip install -r pip-requirements.txt
    #python setup.py develop
    deactivate
```

```{r, engine='bash', install_ckanext-transparencyderp}
    ./usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/
    pip install -e 'git+https://github.com/armin11/ckanext-transparencyderp#egg=ckanext-transparencyderp'
    cd /usr/lib/ckan/default/src/ckanext-transparencyderp/
    #python setup.py develop
    deactivate
```

```{r, engine='bash', symbol_link_schema}
    sudo mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
    sudo ln -s /usr/lib/ckan/default/src/ckanext-transparencyderp/schema.xml /etc/solr/conf/schema.xml
```

```{r, engine='bash', restart_services}
    /etc/init.d/jetty restart
    /etc/init.d/apache2 restart
    /etc/init.d/nginx restart
```

```{r, engine='bash', delete_solr_cache}
    curl http://localhost:8983/solr/update --data '<delete><query>*:*</query></delete>' -H 'Content-type:text/xml; charset=utf-8'
    curl http://localhost:8983/solr/update --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'
```

```{r, engine='bash', reindex_solr}
    ./usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/
    paster --plugin=ckan search-index rebuild -r –config=/etc/ckan/default/production.ini
    deactivate
```

```{r, engine='bash', reindex_solr_problems}
    ./usr/lib/ckan/default/bin/activate
    cd /usr/lib/ckan/default/src/
    paster --plugin=ckan search-index rebuild_fast -r –config=/etc/ckan/default/production.ini
    deactivate
```

Configuration
=============

Set the schemas you want to use with configuration options (ckans .ini file) and activate the search for all packages by default:

```ini
## Search all packages not only dataset
ckan.search.show_all_types = true

ckan.plugins = stats text_view image_view recline_view webpage_view scheming_datasets transparencyderp
# Without ckanext-spatial:
#ckan.plugins = stats text_view image_view recline_view webpage_view spatial_metadata spatial_query scheming_datasets transparencyderp

# Define which views should be created by default
# (plugins must be loaded in ckan.plugins)
ckan.views.default_views = image_view text_view recline_view webpage_view

#   module-path:file to schemas being used
scheming.dataset_schemas = ckanext.transparencyderp:ckan_dataset_rp.json
                           ckanext.transparencyderp:ckan_govdata_full_1_1.json

# scheming.dataset_schemas = http://example.com/spatialx_schema.json

#   Preset files may be included as well. The default preset setting is:
scheming.presets = ckanext.scheming:presets.json

#   The is_fallback setting may be changed as well. Defaults to false:
scheming.dataset_fallback = false
```

If there are proxys, be aware of environment for git and shell!

```{r, engine='bash', reindex_solr_problems}
git config --global http.proxy http://{proxyip}:{proxyport}
git config --global https.proxy http://{proxyip}:{proxyport}
export http_proxy=http://{proxyip}:{proxyport}/
export https_proxy=http://{proxyip}:{proxyport}/
export no_proxy="localhost,127.0.0.1"
#git config --global --unset http.proxy
#git config --global --unset https.proxy
#unset http_proxy
#unset https_proxy
```

Adoption of solr configuration
==============================

An adopted schemal.xml file is included in the root path of the plugin. To show what was altered, see the following snippet:

```xml   
    
    <!-- Extension for ckanext-spatial search via solr 3.1+ -->
    <field name="bbox_area" type="float" indexed="true" stored="true" />
    <field name="maxx" type="float" indexed="true" stored="true" />
    <field name="maxy" type="float" indexed="true" stored="true" />
    <field name="minx" type="float" indexed="true" stored="true" />
    <field name="miny" type="float" indexed="true" stored="true" />

    <!-- field for custom resource choice lists-->
    <field name="res_extras_res_transparency_document_change_classification" type="string" indexed="true" stored="true" multiValued="false"/>

    <dynamicField name="extras_*" type="text" indexed="true" stored="true" multiValued="false"/>
    <dynamicField name="res_extras_*" type="text" indexed="true" stored="true" multiValued="true"/>
    <dynamicField name="vocab_*" type="string" indexed="true" stored="true" multiValued="true"/>
    <dynamicField name="*" type="string" indexed="true"  stored="false"/>
    <field name="transparency_category_de_rp" type="string" indexed="true" stored="true" multiValued="false"/>
    <field name="govdata_categories" type="string" indexed="true" stored="true" multiValued="true"/>
```
