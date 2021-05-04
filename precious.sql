-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 04, 2021 at 10:46 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `precious`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(150) NOT NULL,
  `email` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `bio` varchar(255) DEFAULT NULL,
  `num_sales` int(11) DEFAULT 0,
  `seller_rating` int(11) DEFAULT 0,
  `num_purchases` int(11) DEFAULT 0,
  `profile_picture` varchar(255) DEFAULT NULL,
  `role` varchar(11) DEFAULT 'User'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `email`, `created_at`, `bio`, `num_sales`, `seller_rating`, `num_purchases`, `profile_picture`, `role`) VALUES
(12, 'rootuser', '$pbkdf2-sha256$30000$nNN6rzUGgBCiFCJkrPUe4w$XBlVEeTcZrvgoHylq.fW.UbBEBsoAOiF2FzTSLtPon4', 'Jaredmbenitez@gmail.com', '2021-03-04 06:22:10', NULL, 0, 0, NULL, NULL, NULL),
(13, 'rootuser', '$pbkdf2-sha256$30000$dA4hpNR6r3VOCeEco1RqrQ$AeW84d9JOmveAisPeM4Pf0gi4UomnSVEX4GmmqP8xgk', '124@gmail.com', '2021-03-13 00:22:32', NULL, 0, 0, NULL, NULL, NULL),
(14, 'root', '$pbkdf2-sha256$30000$yNnbO4ewlnJOidGa896bUw$Zym740tbDvFt0qfmcrdiejqKsFjFBs0xg3mjkmv2pK8', '123@gmail.com', '2021-05-04 20:40:47', NULL, 0, 5, NULL, '5130.jpg', 'Admin'),
(15, 'MollyJones97', '$pbkdf2-sha256$30000$hlCKkTLm/B/jPOfc2zsnZA$9X8ti1xe/XBEc7.4YYf9HoL.H9lF.qtdlGHDJSgCw5M', 'molly_jones97@yahoo.com', '2021-04-01 05:39:34', NULL, 0, 0, NULL, NULL, NULL),
(16, 'Jaredbenitez97', '$pbkdf2-sha256$30000$1/r/35tz7h1DCMEYI4RQ6g$4mZU9LtI1cVHlG00S4WDFkK2Hfk.iDV0ZJmVtF7K8Uc', 'Jaredmbenitez@gmail.com', '2021-04-04 07:01:07', NULL, NULL, 0, NULL, NULL, NULL),
(17, 'newUser', '$pbkdf2-sha256$30000$MCakdC5lzDnH.B.DUKq1Fg$NjTvlYJwrUjSTtCGcacPEx.bgQiP9i3zfff13PMSVfY', 'newUser@1243.com', '2021-04-06 17:21:53', NULL, 0, 0, 0, NULL, NULL),
(18, 'BowserThaDog', '$pbkdf2-sha256$30000$/r.XMgZg7F3rHQMgZMyZUw$tiOjBDOmkzXq5qstP8i3qPRwhvbPiYeYCMMGdoQrj9k', 'Bowser123@gmail.com', '2021-04-08 02:41:46', NULL, 0, 0, 0, NULL, NULL),
(20, 'DryDolphin123', '$pbkdf2-sha256$30000$txailPI.B6C01ppz7r231g$QCHI9IDSlQJiVm8SUH1ARboRXkBr5aQJ7C/JhySaY9k', 'DD123@gmail.com', '2021-04-08 02:49:08', NULL, 0, 0, 0, NULL, NULL),
(21, 'DonalGlover123', '$pbkdf2-sha256$30000$jxGCUMpZa00JAeB8733v3Q$rZbiW7P9hxWftFqaz2KNTfxOcxmRI23D9VD4LI04NEM', 'DG123@gmail.com', '2021-04-08 02:55:32', NULL, 0, 0, 0, NULL, NULL),
(22, 'ZanderXX', '$pbkdf2-sha256$30000$m1MK4fyf09oboxTivHcOYQ$lAnuGtHiWTHbiUjqnEewmGiEb1oXknyRf7EChug4Rok', 'ZanderXX@123.com', '2021-04-08 03:12:29', NULL, 0, 0, 0, NULL, NULL),
(41, 'Guest154', '$pbkdf2-sha256$30000$NiZkLIUwppSythZi7D1HaA$70mbPmefUCQN1MiEQxL485bj/1K4JpGobirgwEgTh3Y', 'Guest154 @yahoo.com', '2021-04-24 18:38:21', NULL, 0, 0, 0, NULL, 'GuestUser'),
(42, 'alecd5', '$pbkdf2-sha256$30000$zJnTmhNi7L23NiaEUCplrA$Wd02cktq6G/aRH17IP7/L04tkdf9GSFMuxB225ZbiaQ', 'alec_davila5@yahoo.com', '2021-04-25 19:04:28', NULL, 0, 3, 0, NULL, 'User');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`),
  ADD KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
