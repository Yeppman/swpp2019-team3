import reducer, { signupStatus, signinStatus } from "./auth";
import authConstants from "../actions/actionTypes";

const stubSigningUpUser = {
    email: "my_email@papersfeed.com",
    username: "papersfeed",
    password: "swpp",
};

const stubSigningInUser = {
    email: "my_email@papersfeed.com",
    password: "swpp",
};

describe("Auth reducer", () => {
    it("should return default state", () => {
        const newState = reducer(undefined, {});
        expect(newState).toEqual({
            signupStatus: signupStatus.NONE,
            signinStatus: signinStatus.NONE,
        });
    });

    it("should handle signup success", () => {
        const newState = reducer(undefined, {
            type: authConstants.SIGNUP_SUCCESS,
            user: stubSigningUpUser,
        });
        expect(newState).toEqual({
            signupStatus: signupStatus.SUCCESS,
            signinStatus: signinStatus.NONE,
        });
    });

    it("should handle signup duplicate email", () => {
        const newState = reducer(undefined, {
            type: authConstants.SIGNUP_FAILURE_DUPLICATE_EMAIL,
            user: stubSigningUpUser,
        });
        expect(newState).toEqual({
            signupStatus: signupStatus.DUPLICATE_EMAIL,
            signinStatus: signinStatus.NONE,
        });
    });

    it("should handle signup duplicate username", () => {
        const newState = reducer(undefined, {
            type: authConstants.SIGNUP_FAILURE_DUPLICATE_USERNAME,
            user: stubSigningUpUser,
        });
        expect(newState).toEqual({
            signupStatus: signupStatus.DUPLICATE_USERNAME,
            signinStatus: signinStatus.NONE,
        });
    });


    it("should handle signin success", () => {
        const newState = reducer(undefined, {
            type: authConstants.SIGNIN_SUCCESS,
            user: stubSigningInUser,
        });
        expect(newState).toEqual({
            signupStatus: signupStatus.NONE,
            signinStatus: signinStatus.SUCCESS,
        });
    });

    it("should handle signin user not exist", () => {
        const newState = reducer(undefined, {
            type: authConstants.SIGNIN_FAILURE_USER_NOT_EXIST,
            user: stubSigningInUser,
        });
        expect(newState).toEqual({
            signupStatus: signupStatus.NONE,
            signinStatus: signinStatus.USER_NOT_EXIST,
        });
    });

    it("should handle signin wrong password", () => {
        const newState = reducer(undefined, {
            type: authConstants.SGININ_FAILURE_WRONG_PW,
            user: stubSigningInUser,
        });
        expect(newState).toEqual({
            signupStatus: signupStatus.NONE,
            signinStatus: signinStatus.WRONG_PW,
        });
    });
});
