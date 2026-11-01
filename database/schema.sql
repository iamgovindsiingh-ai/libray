CREATE TABLE authors (
	name VARCHAR(150) NOT NULL, 
	bio TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE book_offers (
	member_id INTEGER, 
	title VARCHAR(200) NOT NULL, 
	author VARCHAR(150) NOT NULL, 
	category VARCHAR(100), 
	condition VARCHAR(50) NOT NULL, 
	offer_type VARCHAR(50) NOT NULL, 
	donor_name VARCHAR(150) NOT NULL, 
	contact_phone VARCHAR(30), 
	contact_whatsapp VARCHAR(30), 
	contact_email VARCHAR(150) NOT NULL, 
	pickup_location VARCHAR(200), 
	description TEXT, 
	status VARCHAR(30) NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, price FLOAT DEFAULT 0.0, image_url VARCHAR(350), 
	PRIMARY KEY (id), 
	FOREIGN KEY(member_id) REFERENCES members (id)
);
CREATE TABLE book_request_upvotes (
	request_id INTEGER NOT NULL, 
	member_id INTEGER NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_request_member_upvote UNIQUE (request_id, member_id), 
	FOREIGN KEY(request_id) REFERENCES book_requests (id), 
	FOREIGN KEY(member_id) REFERENCES members (id)
);
CREATE TABLE book_requests (
	member_id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	author VARCHAR(150) NOT NULL, 
	category VARCHAR(100), 
	reason TEXT, 
	votes_count INTEGER NOT NULL, 
	status VARCHAR(30) NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, contact_phone VARCHAR(30), contact_whatsapp VARCHAR(30), contact_email VARCHAR(150), urgency VARCHAR(20) DEFAULT 'normal', admin_notes TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(member_id) REFERENCES members (id)
);
CREATE TABLE book_reviews (
	book_id INTEGER NOT NULL, 
	member_id INTEGER NOT NULL, 
	rating INTEGER NOT NULL, 
	review_text TEXT, 
	is_verified BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(book_id) REFERENCES books (id), 
	FOREIGN KEY(member_id) REFERENCES members (id)
);
CREATE TABLE books (
	isbn VARCHAR(50) NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	author_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	publisher VARCHAR(200), 
	publication_year INTEGER, 
	quantity INTEGER NOT NULL, 
	available_quantity INTEGER NOT NULL, 
	description TEXT, 
	shelf_location VARCHAR(100), 
	barcode VARCHAR(100), 
	accent_color VARCHAR(30), 
	difficulty_level VARCHAR(50), 
	summary TEXT, 
	key_takeaways TEXT, 
	tags VARCHAR(255), 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_books_isbn UNIQUE (isbn), 
	FOREIGN KEY(author_id) REFERENCES authors (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id)
);
CREATE TABLE categories (
	name VARCHAR(100) NOT NULL, 
	description TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE contact_messages (
	sender_name VARCHAR(150) NOT NULL, 
	sender_email VARCHAR(150) NOT NULL, 
	sender_phone VARCHAR(30), 
	subject VARCHAR(200) NOT NULL, 
	message TEXT NOT NULL, 
	message_type VARCHAR(30) NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	admin_reply TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE fines (
	issue_record_id INTEGER NOT NULL, 
	member_id INTEGER NOT NULL, 
	amount NUMERIC(10, 2) NOT NULL, 
	days_overdue INTEGER NOT NULL, 
	is_paid BOOLEAN NOT NULL, 
	paid_at DATETIME, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (issue_record_id), 
	FOREIGN KEY(issue_record_id) REFERENCES issue_records (id), 
	FOREIGN KEY(member_id) REFERENCES members (id)
);
CREATE TABLE issue_records (
	book_id INTEGER NOT NULL, 
	member_id INTEGER NOT NULL, 
	issue_date DATETIME NOT NULL, 
	due_date DATETIME NOT NULL, 
	return_date DATETIME, 
	status VARCHAR(30) NOT NULL, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(book_id) REFERENCES books (id), 
	FOREIGN KEY(member_id) REFERENCES members (id)
);
CREATE TABLE members (
	user_id INTEGER NOT NULL, 
	student_id VARCHAR(50) NOT NULL, 
	email VARCHAR(150) NOT NULL, 
	phone VARCHAR(30), 
	department VARCHAR(100), 
	year VARCHAR(20), 
	address TEXT, 
	is_active BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_members_student_id UNIQUE (student_id), 
	CONSTRAINT uq_members_email UNIQUE (email), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE TABLE notifications (
	member_id INTEGER NOT NULL, 
	title VARCHAR(150) NOT NULL, 
	message TEXT NOT NULL, 
	type VARCHAR(50) NOT NULL, 
	is_read BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(member_id) REFERENCES members (id)
);
CREATE TABLE reading_notes (
	member_id INTEGER NOT NULL, 
	book_id INTEGER NOT NULL, 
	title VARCHAR(150) NOT NULL, 
	note_text TEXT NOT NULL, 
	quote TEXT, 
	page_number INTEGER, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(member_id) REFERENCES members (id), 
	FOREIGN KEY(book_id) REFERENCES books (id)
);
CREATE TABLE student_badges (
	member_id INTEGER NOT NULL, 
	badge_code VARCHAR(50) NOT NULL, 
	title VARCHAR(100) NOT NULL, 
	description VARCHAR(255) NOT NULL, 
	icon VARCHAR(50) NOT NULL, 
	category VARCHAR(50) NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_member_badge_code UNIQUE (member_id, badge_code), 
	FOREIGN KEY(member_id) REFERENCES members (id)
);
CREATE TABLE study_notes (
	member_id INTEGER, 
	title VARCHAR(200) NOT NULL, 
	subject VARCHAR(150) NOT NULL, 
	department VARCHAR(100), 
	semester VARCHAR(50), 
	description TEXT, 
	author_name VARCHAR(150) NOT NULL, 
	contact_whatsapp VARCHAR(30), 
	contact_phone VARCHAR(30), 
	contact_email VARCHAR(150), 
	file_url VARCHAR(350) NOT NULL, 
	file_type VARCHAR(30) NOT NULL, 
	likes_count INTEGER NOT NULL, 
	downloads_count INTEGER NOT NULL, 
	status VARCHAR(30) NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(member_id) REFERENCES members (id)
);
CREATE TABLE users (
	email VARCHAR(150) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	full_name VARCHAR(150) NOT NULL, 
	role VARCHAR(30) NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_users_email UNIQUE (email)
);
