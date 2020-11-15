class FuseboxApi {
    constructor() {
        this.baseUrl = process.env.REACT_APP_FUSEBOX_API_URL;

        this.headers = {
            'user-agent': 'Fusebox Website',
            'content-type': 'application/json',
            'authorization': 'Bearer ' + this.getAccessToken()
        };
    }

    removeAccessToken() {
        sessionStorage.removeItem('accessToken');
        sessionStorage.removeItem('refreshToken');
    }

    getAccessToken() {
        return sessionStorage.getItem('accessToken');
    }

    setAccessToken(token) {
        return sessionStorage.setItem('accessToken', token);
    }

    getRefreshToken() {
        return sessionStorage.getItem('refreshToken');
    }

    setRefreshToken(token) {
        return sessionStorage.setItem('refreshToken', token);
    }

    async auth(username, password) {
        const response = await fetch(this.baseUrl + '/v1/token/', {
            cache: 'no-cache',
            headers: this.headers,
            method: 'POST',
            redirect: 'follow',
            referrer: 'no-referrer',
            body: JSON.stringify({
                username: username,
                password: password
            }),
        });

        const json = await response.json();

        return json;
    };

    async unratedTracks(offset = 0, limit = 10) {
        const response = await fetch(this.baseUrl + '/v1/tracks/unrated/?limit=' + limit + '&offset=' + offset, {
            cache: 'no-cache',
            headers: this.headers,
            method: 'GET',
            redirect: 'follow',
            referrer: 'no-referrer',
        });

        const json = await response.json();

        return json;
    };

    async searchTracks(q, offset = 0, limit = 10) {
        const response = await fetch(this.baseUrl + '/v1/tracks/search/?q=' + q + '&limit=' + limit + '&offset=' + offset, {
            cache: 'no-cache',
            headers: this.headers,
            method: 'GET',
            redirect: 'follow',
            referrer: 'no-referrer',
        });

        const json = await response.json();

        return json;
    };

    async rateTrack(trackId, score) {
        const response = await fetch(this.baseUrl + '/v1/tracks/' + trackId + '/rate', {
            cache: 'no-cache',
            headers: this.headers,
            method: 'POST',
            redirect: 'follow',
            referrer: 'no-referrer',
            body: JSON.stringify({
                'category': 'like',
                'score': score
            }),
        });

        const json = await response.json();

        return json;
    };

    dumpTracks() {
        fetch(this.baseUrl + '/v1/tracks/dump', {
            cache: 'no-cache',
            headers: this.headers,
            method: 'GET',
            redirect: 'follow',
            referrer: 'no-referrer',
        })
            .then(res => res.blob())
            .then(blob => {
                window.location.assign(window.URL.createObjectURL(blob));
            });
    };

    async detailsTrack(trackId) {
        const response = await fetch(this.baseUrl + '/v1/tracks/' + trackId + '/details', {
            cache: 'no-cache',
            headers: this.headers,
            method: 'GET',
            redirect: 'follow',
            referrer: 'no-referrer',
        });

        const json = await response.json();

        return json;
    };

    async predictionsTrack(trackId) {
        const response = await fetch(this.baseUrl + '/v1/tracks/' + trackId + '/predictions', {
            cache: 'no-cache',
            headers: this.headers,
            method: 'GET',
            redirect: 'follow',
            referrer: 'no-referrer',
        });

        const json = await response.json();

        return json;
    };
}

export default FuseboxApi;