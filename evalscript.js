//VERSION=3
//double curly brackets render as single curly brackets in python format strings

var debug = []

var ic = {{  // index components
  'NDVI':  ["B08", "B04"],
  "GNDVI": ["B08", "B03"],
  "BNDVI": ["B08", "B02"],
  "NDSI":  ["B11", "B12"],
  "NDWI":  ["B03", "B08"]
}}

function setup(ds) {{
  return {{
    input: [{{
      bands: {bands}, 
      units: "DN"
    }}],
    output: {output_array},
    mosaicking: Mosaicking.ORBIT       
  }}
}}

function validate (sample) {{
  if (sample.dataMask!=1) return false;
  
  var scl = Math.round(sample.SCL);
  
  if (scl === 3) {{ // SC_CLOUD_SHADOW
    return false;
  }} else if (scl === 9) {{ // SC_CLOUD_HIGH_PROBA
    return false; 
  }} else if (scl === 8) {{ // SC_CLOUD_MEDIUM_PROBA
    return false;
  }} else if (scl === 7) {{ // SC_CLOUD_LOW_PROBA
    //return false;
  }} else if (scl === 10) {{ // SC_THIN_CIRRUS
    return false;
  }} else if (scl === 11) {{ // SC_SNOW_ICE
    return false;
  }} else if (scl === 1) {{ // SC_SATURATED_DEFECTIVE
    return false;
  }} else if (scl === 2) {{ // SC_DARK_FEATURE_SHADOW
    //return false;
  }}
  return true;
}}

function calculateIndex(a,b)
{{
  if ((a+b)==0) return 0;
  // stretch [-1,+1] to [0,1]
  return ((a-b)/(a+b)+1)/2;
}}

function interpolatedValue(arr)
{{
  //here we define the function on how to define the proper value - e.g. linear interpolation; we will use average 
  if (arr.length==0) return 0;
  if (arr.length==1) return arr[0];
  var sum = 0;
  for (j=0;j<arr.length;j++)
  {{sum+=arr[j];}}
  return Math.round(sum/arr.length);
}}

var results = {results_object}

// We split each month into two halves. This will make it easier to append months to data cube later
var day_of_new_interval = {day_of_new_interval}
var endtime = new Date({enddate_unix}) // UNIX epoch in ms

function evaluatePixel(samples, scenes, inputMetadata, customData, outputMetadata) {{
  
  //Debug part returning "something" if there are no  valid samples (no observations)
  if (!samples.length)
  return {debug_results}
  
  var is_in_last_half_of_month = endtime.getUTCDate() >= day_of_new_interval
  var i = 0; // interval number
  var int_bands = {int_bands}
  
  for (var j = 0; j < samples.length; j++) {{
    
    //TODO order should be reversed when we go leastRecent
    
    // if scene is outside of current half of month, fill result array and change half of month
    // algorithm starts with most recent observation
    if (( !is_in_last_half_of_month && scenes[j].date.getUTCDate() >= day_of_new_interval) ||
    (  is_in_last_half_of_month && scenes[j].date.getUTCDate() <  day_of_new_interval))
    {{
      fillResultArray(i, int_bands)
      
      //reset values
      for (var int_b in int_bands) {{
        int_bands[int_b] = []
      }}
      
      is_in_last_half_of_month = !is_in_last_half_of_month;
      i++;
    }}
    
    if (validate(samples[j]))
    {{
      // push input samples into their respective arrays
      for (var int_b in int_bands) {{
        int_bands[int_b].push(samples[j][int_b])
      }}
    }}
    
  }}
  
  //execute this for the last interval 
  fillResultArray(i, int_bands);
  
  return results
}}

function fillResultArray(i, int_bands)
{{
  for (var b in int_bands) {{
    if(int_bands[b].length==0) results[b][i] = 0
    else results[b][i] = interpolatedValue(int_bands[b])
  }}
  
  for (var ix of {indices}) {{
    if(ic.hasOwnProperty(ix)) {{
      results[ix][i] = 65535*calculateIndex(
        results[ic[ix][0]][i],
        results[ic[ix][1]][i]
      )
    }}
    if(ix==="CVI"){{
      // output sample type for CVI is FLOAT32
      results[ix][i] = results["B08"][i]*results["B05"][i] / (results["B03"][i]*results["B03"][i])
    }}
  }}
}}

function updateOutputMetadata(scenes, inputMetadata, outputMetadata) {{
  outputMetadata.userData = {{
    "date_created": Date(),
    "metadata": scenes.map(s => {{
      s.date = s.date.toString()
      return s
    }}),
    "time" : {avg_times},
    "debug": debug
  }}
}}