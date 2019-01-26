import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import AssesmentIcon from '@material-ui/icons/Assessment';
import AddBoxIcon from '@material-ui/icons/AddBox';
import LocationCityIcon from '@material-ui/icons/LocationCity';
import { Link } from "react-router-dom";

export const CoasterListItems = (
    <div>
      <ListItem component={Link} to="/themeparks/goals" button>
        <ListItemIcon>
          <AssesmentIcon />
        </ListItemIcon>
        <ListItemText primary="Goals" />
      </ListItem>
      <ListItem component={Link} to="/themeparks/goals/new" button>
        <ListItemIcon>
          <AddBoxIcon />
        </ListItemIcon>
        <ListItemText primary="New Goal" />
      </ListItem>
      <ListItem component={Link} to="/themeparks/parks" button>
        <ListItemIcon>
          <LocationCityIcon />
        </ListItemIcon>
        <ListItemText primary="Parks" />
      </ListItem>
    </div>
  );