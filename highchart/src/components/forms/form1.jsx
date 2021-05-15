

import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
const useStyles = makeStyles((theme) => ({
  root: {
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: 200,
    },
  },
}));
export default function Form2(props) {
  // Declare a new state variable, which we'll call "count"
  const classes = useStyles();
  const { setVariabels } = props;
  const [state, setState] = useState({
    'vihicleMass': 1500, 'wheelRadius': 0.314, 'singleSpeedRadius': 6.31, 'rollingRsistance': 0.01,
    'scx': 0.83, 'roadAngle': 0, 'tranEfficiency': 0.95, 'inverterEfficiency': 0.97, 'motorEfficiency': 0.95, 'numberCycle': 3,
  });
  useEffect(() => {
  })
  const onRunSimulation = (e) => {
    // go to next page
    // setVariabels(state);
    fetch('http://localhost:8000/variables', {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(state)
    }).then(res => {
      setVariabels(state);
    }).catch(err => {
      console.log(err)
    })
  }
  const handleChange = (e) => {
    const { name, value } = e.target;
    setState({ ...state, [name]: value });
  }
  return (
    <form className={classes.root} noValidate autoComplete="off">
      <div>
        <TextField
          label="vihicleMass"
          defaultValue={state.vihicleMass}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="vihicleMass"
        />
      </div>
      <div>
        <TextField
          label="wheelRadius"
          defaultValue={state.wheelRadius}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="wheelRadius"
        />
      </div>
      <div>
        <TextField
          label="singleSpeedRadius"
          defaultValue={state.singleSpeedRadius}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="singleSpeedRadius"
        />
      </div>
      <div>
        <TextField
          label="rollingRsistance"
          defaultValue={state.rollingRsistance}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="rollingRsistance"
        />
      </div>
      <div>
        <TextField
          label="scx"
          defaultValue={state.scx}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="scx"
        />
      </div>
      <div>
        <TextField
          label="roadAngle"
          defaultValue={state.roadAngle}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="roadAngle"
        />
      </div>
      <div>
        <TextField
          label="tranEfficiency"
          defaultValue={state.tranEfficiency}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="tranEfficiency"
        />
      </div>
      <div>
        <TextField
          label="inverterEfficiency"
          defaultValue={state.inverterEfficiency}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="inverterEfficiency"
        />
      </div>
      <div>
        <TextField
          label="motorEfficiency"
          defaultValue={state.motorEfficiency}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="motorEfficiency"
        />
      </div>
      <div>
        <TextField
          label="numberCycle"
          defaultValue={state.numberCycle}
          variant="outlined"
          size="small"
          onChange={handleChange}
          name="numberCycle"
        />
      </div>
      <Button variant="contained" color="primary" onClick={onRunSimulation} >
        RUN SIMULATION
      </Button>
    </form>
  );
}
