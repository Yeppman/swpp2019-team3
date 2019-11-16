import React, { Component } from "react";
import { connect } from "react-redux";
import {
    Button, Image, Tabs, Tab,
} from "react-bootstrap";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

import { CollectionCard, ReviewCard } from "../../../components";
import { collectionActions, reviewActions, userActions } from "../../../store/actions";

import "./ProfileDetail.css";
import SamplePhoto from "./sample.jpg";

class ProfileDetail extends Component {
    constructor(props) {
        super(props);
        this.state = {
            collections: [],
            reviews: [],
            followerCount: 0,
            followingCount: 0,
            doIFollow: false,
        };
    }

    componentDidMount() {
        this.props.onGetUser({ id: this.props.location.pathname.split("=")[1] })
            .then(() => {
                this.setState({ doIFollow: this.props.thisUser.is_following });
                if (this.props.thisUser.count) {
                    this.setState({
                        followerCount: this.props.thisUser.count.follower,
                        followingCount: this.props.thisUser.count.following,
                    });
                }
            })
            .catch(() => {});
        this.props.onGetCollections({ id: this.props.location.pathname.split("=")[1] })
            .then(() => {
                this.setState({ collections: this.props.collections });
            })
            .catch(() => {});
        this.props.onGetReviews({ id: this.props.location.pathname.split("=")[1] })
            .then(() => {
                this.setState({ reviews: this.props.reviews });
            })
            .catch(() => {});
    }

    clickFollowHandler = () => {
        this.props.onFollow({ id: this.props.thisUser.id })
            .then(() => {
                this.setState({
                    followerCount: this.props.afterFollowCount,
                    doIFollow: true,
                });
            });
    }

    clickUnfollowHandler = () => {
        this.props.onUnFollow({ id: this.props.thisUser.id })
            .then(() => {
                this.setState({
                    followerCount: this.props.afterUnfollowCount,
                    doIFollow: false,
                });
            });
    }

    collectionCardMaker = (collection) => (
        <CollectionCard
          key={collection.id}
          source={collection.source}
          id={collection.id}
          user={collection.user}
          title={collection.title}
          memberCount={collection.count.users}
          paperCount={collection.count.papers}
          replyCount={collection.replyCount}
          likeCount={collection.count.likes}
          isLiked={collection.liked}
          headerExists={false}
        />
    );

    reviewCardMaker = (review) => (
        <ReviewCard
          key={review.id}
          id={review.id}
          paperId={review.paper.id}
          author={review.user.username}
          title={review.title}
          isLiked={review.liked}
          likeCount={review.count.likes}
          replyCount={review.count.replies}
          headerExists={false}
        />
    );

    render() {
        const settingButton = (
            <Link to="/account_setting">
                <Button id="settingButton">Setting</Button>
            </Link>
        );
        const followButton = (
            <Button
              id="followButton"
              onClick={() => this.clickFollowHandler()}
            >Follow
            </Button>
        );
        const unfollowButton = (
            <Button
              id="unfollowButton"
              onClick={() => this.clickUnfollowHandler()}
            >Unfollow
            </Button>
        );
            // only one button will be displayed among "edit", "follow", and "unfollow" buttons
        let buttonDisplayed;
        if (this.props.me && this.props.me.id === this.props.thisUser.id) {
            buttonDisplayed = settingButton;
        } else if (this.state.doIFollow) {
            buttonDisplayed = unfollowButton;
        } else {
            buttonDisplayed = followButton;
        }

        const collectionCardsLeft = this.state.collections
            .filter((x) => this.state.collections.indexOf(x) % 2 === 0)
            .map((collection) => this.collectionCardMaker(collection));

        const collectionCardsRight = this.state.collections
            .filter((x) => this.state.collections.indexOf(x) % 2 === 1)
            .map((collection) => this.collectionCardMaker(collection));

        const reviewCardsLeft = this.state.reviews
            .filter((x) => this.state.reviews.indexOf(x) % 2 === 0)
            .map((review) => this.reviewCardMaker(review));

        const reviewCardsRight = this.state.reviews
            .filter((x) => this.state.reviews.indexOf(x) % 2 === 1)
            .map((review) => this.reviewCardMaker(review));

        return (
            <div className="ProfileDetail">
                <div className="ProfileDetailContent">
                    <div className="userInfo">
                        <div className="userStatistic">
                            <div className="userPhotoName">
                                <Image id="userPhoto" src={SamplePhoto} width={150} height={150} roundedCircle />
                                <h2 id="userName">{this.props.thisUser.username}</h2>
                            </div>
                            <div id="collectionStat">
                                <h5 id="collectionCount">{this.state.collections.length}</h5>
                                <h5 id="collectionText">Collections</h5>
                            </div>
                            <div id="reviewStat">
                                <h5 id="reviewCount">{this.state.reviews.length}</h5>
                                <h5 id="reviewText">Reviews</h5>
                            </div>
                            <Link id="followerStat" to={`/profile_id=${this.props.thisUser.id}/followers`}>
                                <h5 id="followerCount">{this.state.followerCount}</h5>
                                <h5 id="followerText">Follower</h5>
                            </Link>
                            <Link id="followingStat" to={`/profile_id=${this.props.thisUser.id}/followings`}>
                                <h5 id="followingCount">{this.state.followingCount}</h5>
                                <h5 id="followingText">Following</h5>
                            </Link>
                        </div>
                        <div className="userDescAndButton">
                            <div id="buttonDisplayed">{buttonDisplayed}</div>
                            <p id="userDescription">{this.props.thisUser.description}</p>
                        </div>
                    </div>
                    <div className="itemTabSection">
                        <Tabs defaultActiveKey="collectionTab" id="itemTabs">
                            <Tab eventKey="collectionTab" title="Collections">
                                <div id="collectionCards">
                                    <div id="collectionCardsLeft">{collectionCardsLeft}</div>
                                    <div id="collectionCardsRight">{collectionCardsRight}</div>
                                </div>
                            </Tab>
                            <Tab eventKey="reviewTab" title="Reviews">
                                <div id="reviewCards">
                                    <div id="reviewCardsLeft">{reviewCardsLeft}</div>
                                    <div id="reviewCardsRight">{reviewCardsRight}</div>
                                </div>
                            </Tab>
                        </Tabs>
                    </div>
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state) => ({
    me: state.auth.me,
    collections: state.collection.list.list,
    reviews: state.review.list.list,
    thisUser: state.user.selectedUser,
    afterFollowCount: state.user.followCount,
    afterUnfollowCount: state.user.unfollowCount,
});

const mapDispatchToProps = (dispatch) => ({
    onGetUser: (userId) => dispatch(userActions.getUserByUserId(userId)),
    onGetCollections: (userId) => dispatch(collectionActions.getCollectionsByUserId(userId)),
    onGetReviews: (userId) => dispatch(reviewActions.getReviewsByUserId(userId)),
    onFollow: (targetId) => dispatch(userActions.addUserFollowing(targetId)),
    onUnFollow: (targetId) => dispatch(userActions.removeUserFollowing(targetId)),
});

export default connect(mapStateToProps, mapDispatchToProps)(ProfileDetail);

ProfileDetail.propTypes = {
    location: PropTypes.objectOf(PropTypes.any),
    me: PropTypes.objectOf(PropTypes.any),
    thisUser: PropTypes.objectOf(PropTypes.any),
    collections: PropTypes.arrayOf(PropTypes.any),
    reviews: PropTypes.arrayOf(PropTypes.any),
    onGetCollections: PropTypes.func,
    onGetReviews: PropTypes.func,
    onGetUser: PropTypes.func,
    onFollow: PropTypes.func,
    onUnFollow: PropTypes.func,
    afterFollowCount: PropTypes.number,
    afterUnfollowCount: PropTypes.number,
};

ProfileDetail.defaultProps = {
    location: null,
    me: null,
    thisUser: {},
    collections: [],
    reviews: [],
    onGetCollections: () => {},
    onGetReviews: () => {},
    onGetUser: () => {},
    onFollow: () => {},
    onUnFollow: () => {},
    afterFollowCount: 0,
    afterUnfollowCount: 0,
};