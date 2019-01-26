import React from 'react';
import { Paper, Typography } from '@material-ui/core';

class Carousel extends React.Component {
    componentDidMount() {

    }

    render() {
        return (
            <div className="goalCarousel">
                {React.Children.map(this.props.children, (slide, index) => {
                    return React.cloneElement(slide, {
                        style: { display: index === this.props.showIndex ? 'block' : 'none' }
                    })
                })}
            </div>
        )
    }
}

export default Carousel;