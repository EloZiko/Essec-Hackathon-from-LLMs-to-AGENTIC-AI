// pages/index.js
'use client';
import { useState } from 'react';
import Head from 'next/head';
import Image from 'next/image';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [rating, setRating] = useState(0);
  const [hover, setHover] = useState(0);
  const [submitted, setSubmitted] = useState(false);
  const [comment, setComment] = useState('');

  const handleSubmit = () => {
    let avis = [{note : rating},{commentaire : comment}];
    let json = JSON.stringify(avis);
    // envoyer le json au modèle
    setSubmitted(true);
  };

  const renderReviewForm = () => {
    return (
      <div className={styles.reviewContainer}>
        <div className={styles.imageAndTitle}>
          <div className={styles.imageContainer}>
            <Image
              src="/tour-de-pise-toscane.jpg"
              alt="Tour de Pize"
              width={240}
              height={180}
              layout="responsive"
              objectFit="cover"
            />
          </div>
          <h1 className={styles.title}>Tour de Pize</h1>
        </div>

        <div className={styles.questionContainer}>
          <p className={styles.question}>Quel est votre avis sur cet endroit ?</p>
        </div>

        <div className={styles.starsContainer}>
          {[...Array(5)].map((_, index) => {
            const starValue = index + 1;
            return (
              <button
                type="button"
                key={index}
                className={styles.starButton}
                onClick={() => setRating(starValue)}
                onMouseEnter={() => setHover(starValue)}
                onMouseLeave={() => setHover(0)}
              >
                <span className={`${styles.star} ${(hover || rating) >= starValue ? styles.filled : styles.empty}`}>
                  ★
                </span>
              </button>
            );
          })}
        </div>

        <div className={styles.commentBox}>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder=""
            className={styles.textarea}
          />
        </div>

        <button onClick={handleSubmit} className={styles.submitButton}>
          Valider
        </button>
      </div>
    );
  };

  const renderThankYouScreen = () => {
    return (
      <div className={styles.thankYouContainer}>
        <div className={styles.thumbContainer}>
          <span className={styles.thumbIcon}>👍</span>
        </div>
        <p className={styles.thankYouText}>Merci de votre réponse !</p>
      </div>
    );
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Tour de Pise - Avis</title>
        <meta name="description" content="Donnez votre avis sur la Tour de Pize" />
        <link rel="icon" href="/favicon.ico" />
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet" />
      </Head>

      <main className={`${styles.main} ${submitted ? styles.mainSubmitted : ''}`}>
        <div className={styles.card}>
          {!submitted ? renderReviewForm() : renderThankYouScreen()}
        </div>
      </main>
    </div>
  );
}
