{#
    This macro computes the specified percentile value over a specified partition window. 
#}
{% macro bigquery__quantile(field, quantile, partition) -%}
    percentile_cont({{ field }}, {{ quantile }})
    over({%- if partition %}partition by {{ partition }}{% endif -%})
{% endmacro %}