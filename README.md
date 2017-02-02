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
