"use client"
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Heart, X, Search, Check } from 'lucide-react';
import Head from 'next/head';
import Image from 'next/image';
import styles from '../../styles/Home.module.css';

// Définition de l'interface pour les destinations
interface Destination {
  id: number;
  name: string;
  location: string;
  description: string;
  image: string;
}

export default function Home() {
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [likedDestinations, setLikedDestinations] = useState<Destination[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [appState, setAppState] = useState('search'); // 'search', 'swipe', 'results'
  const [isSearching, setIsSearching] = useState(false);
  
  // Simuler le chargement des destinations
  useEffect(() => {
    if (appState === 'swipe' && !destinations.length) {
      setIsSearching(true);
      // Simuler un délai de chargement API
      setTimeout(() => {
        const mockDestinations: Destination[] = [
          {
            id: 1,
            name: "Tour Eiffel",
            location: "Paris, France",
            description: "Symbole de Paris, offrant une vue panoramique exceptionnelle sur la ville.",
            image: "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f"
          },
          {
            id: 2,
            name: "Musée du Louvre",
            location: "Paris, France",
            description: "Le plus grand musée d'art et d'antiquités au monde, abritant la Joconde.",
            image: "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f"
          },
          {
            id: 3,
            name: "Château de Versailles",
            location: "Versailles, France",
            description: "Ancienne résidence royale célèbre pour ses jardins et son architecture.",
            image: "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f"
          },
          {
            id: 4,
            name: "Mont Saint-Michel",
            location: "Normandie, France",
            description: "Une île-monastère médiévale magnifique avec une architecture gothique.",
            image: "https://images.unsplash.com/photo-1531572753322-ad063cecc140"
          },
          {
            id: 5,
            name: "Côte d'Azur",
            location: "Sud de la France",
            description: "Magnifiques plages méditerranéennes et villes balnéaires luxueuses.",
            image: "https://images.unsplash.com/photo-1527824404775-dce343118ebc"
          },
        ];
        setDestinations(mockDestinations);
        setIsSearching(false);
      }, 1500);
    }
  }, [appState, destinations.length]);

  // Surveiller la fin du swipe pour passer aux résultats
  useEffect(() => {
    if (appState === 'swipe' && destinations.length > 0 && currentIndex >= destinations.length) {
      // Animation de transition vers les résultats
      const timer = setTimeout(() => {
        setAppState('results');
      }, 800);
      return () => clearTimeout(timer);
    }
  }, [currentIndex, destinations.length, appState]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setLikedDestinations([]);
    setCurrentIndex(0);
    setDestinations([]);
    setAppState('swipe');
  };

  const swiped = (direction: 'left' | 'right') => {
    if (direction === 'right') {
      setLikedDestinations([...likedDestinations, destinations[currentIndex]]);
    }
    
    setCurrentIndex(currentIndex + 1);
  };

  const handleLike = () => {
    swiped('right');
  };

  const handleDislike = () => {
    swiped('left');
  };

  const resetSearch = () => {
    setSearchTerm('');
    setCurrentIndex(0);
    setLikedDestinations([]);
    setDestinations([]);
    setAppState('search');
  };

  // Animations pour les transitions entre états
  const pageVariants = {
    initial: { opacity: 0, y: 20 },
    in: { opacity: 1, y: 0 },
    out: { opacity: 0, y: -20 }
  };

  const pageTransition = {
    type: "tween",
    ease: "anticipate",
    duration: 0.5
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Travel Swiper</title>
        <meta name="description" content="Découvrez des destinations et swipez pour créer votre itinéraire!" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <motion.main 
        className={styles.main}
        initial="initial"
        animate="in"
        variants={pageVariants}
        transition={pageTransition}
      >
        <header className={styles.header}>
          <motion.h1 
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 120 }}
          >
            ✈️ Travel Swiper
          </motion.h1>
          <motion.p
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            Découvrez des destinations et créez votre itinéraire de rêve
          </motion.p>
        </header>

        <AnimatePresence mode="wait">
          {appState === 'search' && (
            <motion.div 
              className={styles.searchContainer}
              key="search"
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <form className={styles.searchForm} onSubmit={handleSearch}>
                <motion.div 
                  className={styles.inputWrapper}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.6 }}
                >
                  <Search size={20} className={styles.searchIcon} />
                  <input
                    type="text"
                    placeholder="Où souhaitez-vous voyager?"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className={styles.searchInput}
                  />
                  <motion.button 
                    type="submit"
                    whileHover={{ scale: 1.03 }}
                    whileTap={{ scale: 0.97 }}
                  >
                    Découvrir
                  </motion.button>
                </motion.div>
              </form>
              
              <motion.div 
                className={styles.searchHint}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1 }}
              >
                <p>Essayez "France", "Paris" ou "Plage"</p>
              </motion.div>
            </motion.div>
          )}

          {appState === 'swipe' && (
            <motion.div 
              className={styles.swipeContainer}
              key="swipe"
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              {isSearching ? (
                <motion.div 
                  className={styles.loadingContainer}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <div className={styles.loadingSpinner}></div>
                  <p>Recherche des meilleures destinations...</p>
                </motion.div>
              ) : destinations.length > 0 && currentIndex < destinations.length ? (
                <>
                  <motion.div
                    className={styles.swipeProgress}
                    initial={{ width: 0 }}
                    animate={{ width: `${(currentIndex / destinations.length) * 100}%` }}
                  />
                  
                  <motion.p className={styles.swipeCounter}>
                    {currentIndex + 1} / {destinations.length}
                  </motion.p>
                
                  <AnimatePresence>
                    <motion.div 
                      className={styles.card}
                      key={destinations[currentIndex].id}
                      initial={{ scale: 0.8, opacity: 0, rotateZ: -5 }}
                      animate={{ scale: 1, opacity: 1, rotateZ: 0 }}
                      exit={{ 
                        x: 300, 
                        opacity: 0,
                        transition: { duration: 0.3 }
                      }}
                      drag="x"
                      dragConstraints={{ left: 0, right: 0 }}
                      dragElastic={1}
                      onDragEnd={(e, { offset, velocity }) => {
                        const swipe = offset.x > 100 ? 'right' : offset.x < -100 ? 'left' : null;
                        if (swipe) {
                          swiped(swipe);
                        }
                      }}
                    >
                      <div 
                        className={styles.cardImage} 
                        style={{ position: 'relative', width: '100%', height: '300px' }}
                      >
                        <Image 
                          src={destinations[currentIndex].image}
                          alt={destinations[currentIndex].name}
                          fill
                          style={{ objectFit: 'cover' }}
                          priority
                        />
                        <div className={styles.cardGradient}></div>
                      </div>
                      <div className={styles.cardContent}>
                        <h2>{destinations[currentIndex].name}</h2>
                        <p className={styles.location}>{destinations[currentIndex].location}</p>
                        <p className={styles.description}>{destinations[currentIndex].description}</p>
                      </div>
                      <div className={styles.swipeInstruction}>
                        <motion.p 
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.5 }}
                        >
                          ← Glissez ou utilisez les boutons →
                        </motion.p>
                      </div>
                    </motion.div>
                  </AnimatePresence>

                  <div className={styles.swipeButtons}>
                    <motion.button 
                      className={styles.dislikeBtn} 
                      onClick={handleDislike}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      <X size={30} />
                    </motion.button>
                    <motion.button 
                      className={styles.likeBtn} 
                      onClick={handleLike}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      <Heart size={30} />
                    </motion.button>
                  </div>
                </>
              ) : null}
            </motion.div>
          )}

          {appState === 'results' && (
            <motion.div 
              className={styles.resultsContainer}
              key="results"
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <motion.div
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <div className={styles.resultsHeader}>
                  <h2>Votre itinéraire de voyage</h2>
                  {likedDestinations.length > 0 && (
                    <motion.div 
                      className={styles.resultsCheck}
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ delay: 0.8, type: "spring" }}
                    >
                      <Check size={20} />
                    </motion.div>
                  )}
                </div>
              </motion.div>

              {likedDestinations.length > 0 ? (
                <motion.div 
                  className={styles.likedGrid}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  {likedDestinations.map((destination, index) => (
                    <motion.div 
                      className={styles.likedCard} 
                      key={destination.id}
                      initial={{ y: 50, opacity: 0 }}
                      animate={{ 
                        y: 0, 
                        opacity: 1,
                        transition: { delay: 0.2 + index * 0.1 }
                      }}
                    >
                      <div className={styles.likedImg} style={{ position: 'relative', width: '100%', height: '200px' }}>
                        <Image
                          src={destination.image}
                          alt={destination.name}
                          fill
                          style={{ objectFit: 'cover' }}
                        />
                        <div className={styles.likedBadge}>
                          <Heart size={16} />
                        </div>
                      </div>
                      <div className={styles.likedContent}>
                        <h3>{destination.name}</h3>
                        <p className={styles.location}>{destination.location}</p>
                        <p>{destination.description}</p>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              ) : (
                <motion.div 
                  className={styles.noLikes}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  <p>Vous n'avez aimé aucune destination.</p>
                </motion.div>
              )}
              
              <motion.button 
                className={styles.newSearchBtn}
                onClick={resetSearch}
                initial={{ y: 30, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Nouvelle recherche
              </motion.button>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.main>
    </div>
  );
}