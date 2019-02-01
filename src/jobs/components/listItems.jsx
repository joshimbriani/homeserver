import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import AddBoxIcon from '@material-ui/icons/AddBox';
import { Link } from "react-router-dom";

export const JobsListItems = (
    <div>
      <ListItem component={Link} to="/jobs/new" button>
        <ListItemIcon>
          <AddBoxIcon />
        </ListItemIcon>
        <ListItemText primary="New Job" />
      </ListItem>
    </div>
  );