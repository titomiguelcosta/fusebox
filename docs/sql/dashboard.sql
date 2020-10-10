--- Total Played Songs
select count(p.id) from api_played p;

--- Total Rates
select count(r.id) from api_rate r;

--- Top Rating Users
select u.first_name, count(r.user_id) as votes from auth_user u
	inner join api_rate r on u.id = r.user_id
	group by r.user_id
	order by votes desc;

--- Top Played Songs by number of times it played
select t.title as song, t.album, a.name as artist, count(distinct p.id) as played, count(distinct r.id) as votes, avg(r.score) as score from api_track t
	inner join api_track_artists ta on ta.track_id = t.id
	inner join api_artist a on a.id = ta.artist_id
	inner join api_played p on p.track_id = t.id
	inner join api_rate r on r.track_id = t.id
	group by p.track_id
	order by played desc;

--- Top Played Songs by number of rates
select t.title as song, t.album, a.name as artist, count(distinct p.id) as played, count(distinct r.id) as votes, avg(r.score) as score from api_track t
	inner join api_track_artists ta on ta.track_id = t.id
	inner join api_artist a on a.id = ta.artist_id
	inner join api_played p on p.track_id = t.id
	inner join api_rate r on r.track_id = t.id
	group by p.track_id
	order by votes desc;

--- Top Played Songs by best rating
select t.title as song, t.album, a.name as artist, count(distinct p.id) as played, count(distinct r.id) as votes, avg(r.score) as score from api_track t
	inner join api_track_artists ta on ta.track_id = t.id
	inner join api_artist a on a.id = ta.artist_id
	inner join api_played p on p.track_id = t.id
	inner join api_rate r on r.track_id = t.id
	group by p.track_id
	order by score desc;

--- People that unsubscribed
select u.first_name from auth_user u
    inner join api_userprofile up on up.user_id = u.id
    where
        up.notifications = 0
        and u.is_active = 1;
