import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.scheming import helpers as scheming_helpers
from ckan.lib.plugins import DefaultTranslation
import json

class TransparencyderpPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    #new for own translation .po file
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IFacets)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'transparencyderp')

    # define own helpers for doing the translation of the facets from the schema definition
    def get_helpers(self):
        return {
            'transparencyderp_pull_facet_title_from_schema': self._pull_facet_title_from_schema,
            'transparencyderp_pull_title_from_schema': self._pull_title_from_schema
        }

    # function to do the translations for schema information like classifications, ...
    def _pull_facet_title_from_schema(self, package_type, name, item_name, title):
        schema = scheming_helpers.scheming_get_dataset_schema(package_type)
	language = scheming_helpers.lang()
	schema_name = name
	schema_name = schema_name.replace('res_extras_', '')
        # switch for dataset or resource 
        if schema_name.startswith( 'res_' ):
            fields_from_schema = schema['resource_fields']
        else:
            fields_from_schema = schema['dataset_fields']    
        for field in fields_from_schema:
            if field['field_name'] == schema_name:
                #if item key is given - see facet_list.html
                if item_name is not None:
                    if 'choices' in field:
                        for entry in field['choices']:
		            if entry['value'] == item_name:
                                if len(entry['label']) > 1 and type(entry['label']) is dict:
                                    label_array = entry['label']
                                    for key, value in label_array.iteritems():
                                        if key == language:
                                            if value is not None:
                                                return value
                                            else:
                                                return title
                                    if value is not None:
                                        return value
                                    else:
                                        return title
                    else:
                        return title;    
                else:
                    if len(field['label']) > 1 and type(field['label']) is dict:
                        label_array = field['label']
                        for key, value in label_array.iteritems():
                            if key == language:
                                if value is not None:
                                    return value
                                else:
                                    return title
                        if value is not None:
                            return value
                        else:
                            return title
                    if field['label'] is not None:
                        return field['label']
                    else:
                        return title
        return title
    
    #function to get schema title in the right language
    def _pull_title_from_schema(self, package_type):
        language = scheming_helpers.lang()
        schema = scheming_helpers.scheming_get_dataset_schema(package_type)
        if 'dataset_type_label' in schema:
            if len(schema['dataset_type_label']) > 1 and type(schema['dataset_type_label']) is dict:
                label_array = schema['dataset_type_label']
                for key, value in label_array.iteritems():
                    if key == language:
                        if value is not None:
                            return value
                        else:
                            return schema['dataset_type']
                        if value is not None:
                            return value
                        else:
                            return schema['dataset_type']
        else:
            return schema['dataset_type']
    
    #function to define further facets and their translations in the result window when search for dataset/package
    def dataset_facets(self, facets_dict, package_type):
        facets_dict['transparency_category_de_rp'] = toolkit._('transparency classification')
        facets_dict['govdata_categories'] = toolkit._('govdata classification')
	facets_dict['res_extras_res_transparency_document_change_classification'] = toolkit._('doc change classification')
	#facets_dict['dataset_type'] = toolkit._('Dataset type')
	#facets_dict['entity_type'] = toolkit._('Entity type')
        return facets_dict

    #function to define further facets and their translations in the result window when search for group packages
    def group_facets(self, facets_dict, group_type, package_type):
        facets_dict['transparency_category_de_rp'] = toolkit._('transparency classification')
        facets_dict['govdata_categories'] = toolkit._('govdata classification')
        facets_dict['res_extras_res_transparency_document_change_classification'] = toolkit._('doc change classification')
        # facets_dict['dataset_type'] = toolkit._('Dataset type')
        # self._update_facets(facets_dict)
        return facets_dict

    #function to define further facets and their translations in the result window when search for organization packages
    def organization_facets(self, facets_dict, organization_type, package_type):
        facets_dict['transparency_category_de_rp'] = toolkit._('transparency classification')
        facets_dict['govdata_categories'] = toolkit._('govdata classification')
        facets_dict['res_extras_res_transparency_document_change_classification'] = toolkit._('doc change classification')
        #facets_dict['dataset_type'] = toolkit._('Dataset type')
        # self._update_facets(facets_dict)
        return facets_dict   

    #def _update_facets(self, facets_dict):
    #    if 'transparency_category_de_rp' not in factes_dict:
    #        facets_dict.update({
    #            'transparency_category_de_label': plugins.toolkit._('Transparenzportal Kategorien')
    #        })

    #function to multiplex/de-multiplex array before give it to solr index! This is only used for multi select classifications!
    def before_index(self, data_dict):
        #no array any longer, cause it has only one choosable value
        #data_dict['transparency_category_de_rp'] = json.loads(data_dict.get('transparency_category_de_rp', '[]'))
        data_dict['govdata_categories'] = json.loads(data_dict.get('govdata_categories', '[]'))
        return data_dict

