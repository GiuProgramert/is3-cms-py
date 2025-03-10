import React from 'react'
import CanvasJSReact from '@canvasjs/react-charts';
//var CanvasJSReact = require('@canvasjs/react-charts');



// var CanvasJSReact = require('@canvasjs/react-charts');
export const CanvasCustomChart = ({
    title,
    data,
    type,
    width,
    height
}) => {
    // var CanvasJS = CanvasJSReact.CanvasJS;
    var CanvasJSChart = CanvasJSReact.CanvasJSChart;
    const options = {
        animationEnabled: true,
        exportEnabled: true,
        theme: "light2", //"light1", "dark1", "dark2"
        title: {
            text: title,
        },
        axisY: {
            includeZero: true
        },
        
        data: [{
            type: type, //change type to bar, line, area, pie, etc
            //indexLabel: "{y}", //Shows y value on all Data Points
            indexLabelFontColor: "#5A5757",
            indexLabelPlacement: "outside",
            dataPoints: data
        }]
    }

    return (
        <div>
            <CanvasJSChart options={options}
            /* onRef={ref => this.chart = ref} */
             containerProps={{ width: width, height: height }} 
            />
            {/*You can get reference to the chart instance as shown above using onRef. This allows you to access all chart properties and methods*/}

        </div>
    );
}
