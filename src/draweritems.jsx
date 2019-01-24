import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import DashboardIcon from '@material-ui/icons/Dashboard';
import RowingIcon from '@material-ui/icons/Rowing';
import MonetizationOnIcon from '@material-ui/icons/MonetizationOn';
import LibraryMusicIcon from '@material-ui/icons/LibraryMusic';
import CodeIcon from '@material-ui/icons/Code';
import TrainIcon from '@material-ui/icons/Train';
import WebIcon from '@material-ui/icons/Web';
import AssignmentIcon from '@material-ui/icons/Assignment';
import CalendarIcon from '@material-ui/icons/CalendarToday';
import { Link } from "react-router-dom";

export const mainListItems = (
  <div>
    <ListItem component={Link} to="/" button>
      <ListItemIcon>
        <DashboardIcon />
      </ListItemIcon>
      <ListItemText primary="Dashboard" />
    </ListItem>
    <ListItem button>
      <ListItemIcon>
        <CalendarIcon />
      </ListItemIcon>
      <ListItemText primary="Important Today" />
    </ListItem>
  </div>
);

export const secondaryListItems = (
  <div>
    <ListSubheader inset>Saved reports</ListSubheader>
    <ListItem component={Link} to="/about" button>
      <ListItemIcon>
        <AssignmentIcon />
      </ListItemIcon>
      <ListItemText primary="Tasks" />
    </ListItem>
    <ListItem component={Link} to="/users" button>
      <ListItemIcon>
        <RowingIcon />
      </ListItemIcon>
      <ListItemText primary="Health" />
    </ListItem>
    <ListItem component={Link} to="/themeparks" button>
      <ListItemIcon>
        <TrainIcon />
      </ListItemIcon>
      <ListItemText primary="Theme Parks" />
    </ListItem>
    <ListItem component={Link} to="/users" button>
      <ListItemIcon>
        <WebIcon />
      </ListItemIcon>
      <ListItemText primary="Websites" />
    </ListItem>
    <ListItem component={Link} to="/about" button>
      <ListItemIcon>
        <MonetizationOnIcon />
      </ListItemIcon>
      <ListItemText primary="Money" />
    </ListItem>
    <ListItem component={Link} to="/users" button>
      <ListItemIcon>
        <LibraryMusicIcon />
      </ListItemIcon>
      <ListItemText primary="Music" />
    </ListItem>
    <ListItem component={Link} to="/about" button>
      <ListItemIcon>
        <CodeIcon />
      </ListItemIcon>
      <ListItemText primary="Code" />
    </ListItem>
  </div>
);
