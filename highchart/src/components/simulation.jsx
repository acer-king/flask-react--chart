import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import { useDispatch } from "react-redux";
import reduxAction from '../redux/reduxAction';
import Chart from './chat';
const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
}));

export default function Simulation(props) {
  const dispatch = useDispatch();
  const { setFlag } = props
  const classes = useStyles();

  const callDatas = () => {
    fetch('http://localhost:8000/datas', {
      method: 'GET',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      }
    }).then(res => {
      // call redux
      res.json().then(data => {
        reduxAction(dispatch, { type: "SET_LOADING_STATE", arg: false });
        reduxAction(dispatch, { type: "SET_DATA", arg: data });
      })
        .catch(err => {
          reduxAction(dispatch, { type: "SET_LOADING_STATE", arg: false });
        })
    })
      .catch(err => {
        reduxAction(dispatch, { type: "SET_LOADING_STATE", arg: false });
        console.log(err);
      })
  }
  const handleChange = (ev) => {
    ev.preventDefault();
    const data = new FormData();
    data.append('file', ev.target.files[0]);
    reduxAction(dispatch, { type: "SET_LOADING_STATE", arg: true });
    fetch('http://localhost:8000/upload', { method: 'POST', body: data })
      .then((response) => {
        response.json().then((body) => {
          if (body['success']) {
            callDatas();
          }
          else {
            reduxAction(dispatch, { type: "SET_LOADING_STATE", arg: false });
          }
        })
          .catch(err => {
            console.log(err);
            reduxAction(dispatch, { type: "SET_LOADING_STATE", arg: false });
          });
      });
  }
  const onPrev = (e) => {
    // 
    setFlag(false);
  }
  // Create a reference to the hidden file input element
  const hiddenFileInput = React.useRef(null);

  // Programatically click the hidden file input element
  // when the Button component is clicked
  const onLoadFile = event => {
    hiddenFileInput.current.click();
  };

  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Chart></Chart>
        </Grid>
        <Grid item xs={6}>
          <Button variant="contained" color="primary" onClick={onLoadFile} >
            Load Data File
          </Button>
          <input
            type="file"
            ref={hiddenFileInput}
            onChange={handleChange}
            style={{ display: 'none' }}
          />
        </Grid>
        <Grid item xs={6}>
          <Button variant="contained" color="primary" onClick={onPrev} >
            Prev
          </Button>
        </Grid>
      </Grid>
    </div>
  );
}
